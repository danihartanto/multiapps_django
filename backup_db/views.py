import os
import subprocess
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

BACKUP_DIR = os.path.join(settings.MEDIA_ROOT, "backup")
os.makedirs(BACKUP_DIR, exist_ok=True)


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
def index(request):
    backups = []
    for filename in sorted(os.listdir(BACKUP_DIR), reverse=True):
        full_path = os.path.join(BACKUP_DIR, filename)
        if os.path.isfile(full_path):
            backups.append({
                "name": filename,
                "size": os.path.getsize(full_path),
                "path": full_path
            })

    context = {
        'backups': backups
    }
    return render(request, 'backup_db/index.html', context)

@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
def backup_database(request):
    if request.method != "POST":
        return HttpResponse(status=405)  # method not allowed

    tanggal = now().strftime("%Y_%m_%d_%H_%M_%S")
    backup_dir = os.path.join(settings.MEDIA_ROOT, "backup")
    os.makedirs(backup_dir, exist_ok=True)

    db = settings.DATABASES['default']
    backup_file = os.path.join(backup_dir, f"backup_{tanggal}.sql")

    if 'mysql' in db['ENGINE']:
        cmd = [
            'mysqldump',
            f"-u{db['USER']}",
            f"-h{db.get('HOST', 'localhost')}",
            f"-P{db.get('PORT', 3308)}",
            db['NAME']
        ]
        with open(backup_file, 'w') as out:
            result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return HttpResponse(f"Gagal backup DB: {result.stderr}", status=500)
    else:
        return HttpResponse("Hanya mendukung MySQL.")

    messages.success(request, f"Backup berhasil: {os.path.basename(backup_file)}")
    request.session['backup_file_path'] = backup_file
    return redirect('backup_db')

@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
def download_backup(request, filename):
    full_path = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, 'rb'), as_attachment=True, filename=filename)
    return HttpResponse("File tidak ditemukan.", status=404)

@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
def delete_backup(request, filename):
    full_path = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(full_path):
        os.remove(full_path)
        messages.success(request, f"Backup '{filename}' berhasil dihapus.")
    else:
        messages.warning(request, f"File '{filename}' tidak ditemukan.")
    return redirect('backup_db')