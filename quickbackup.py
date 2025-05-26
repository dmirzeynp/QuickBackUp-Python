import os
import pyzipper
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.source_dir = ''
        self.backup_dir = ''
        self.password = ''
        self.backup_history_file = "backup_history.txt"
        self.load_backup_history()
        self.root.title("QuickBackUp")
        self.create_widgets()

    def load_backup_history(self):
        if os.path.exists(self.backup_history_file):
            with open(self.backup_history_file, "r") as f:
                self.backup_history = [line.strip() for line in f.readlines()]
        else:
            self.backup_history = []

    def save_backup_history(self):
        with open(self.backup_history_file, "w") as f:
            for backup in self.backup_history:
                f.write(f"{backup}\n")

    def create_widgets(self):
        tk.Label(self.root, text="Yedeklenecek Klasör Yolu").grid(row=0, column=0)
        self.source_entry = tk.Entry(self.root, width=40)
        self.source_entry.grid(row=0, column=1)
        tk.Button(self.root, text="Gözat", command=self.browse_source).grid(row=0, column=2)

        tk.Label(self.root, text="Yedekleme Klasörü Yolu").grid(row=1, column=0)
        self.backup_entry = tk.Entry(self.root, width=40)
        self.backup_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Gözat", command=self.browse_backup).grid(row=1, column=2)

        tk.Label(self.root, text="Şifre").grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, width=40, show="*")
        self.password_entry.grid(row=2, column=1)

        self.backup_button = tk.Button(self.root, text="Yedekle", command=self.start_backup_thread)
        self.backup_button.grid(row=3, column=0, columnspan=3)

        self.status_label = tk.Label(self.root, text="Durum: Hazır", fg="black")
        self.status_label.grid(row=4, column=0, columnspan=3)

        self.view_backups_button = tk.Button(self.root, text="📁 Önceki Yedekleri Göster", command=self.show_previous_backups)
        self.view_backups_button.grid(row=5, column=0, columnspan=3)

        self.delete_backups_button = tk.Button(self.root, text="🗑️ Önceki Yedekleri Sil", command=self.delete_previous_backups)
        self.delete_backups_button.grid(row=6, column=0, columnspan=3)

        self.clear_button = tk.Button(self.root, text="🧹 İşlemi Bitir / Temizle", command=self.clear_fields)
        self.clear_button.grid(row=7, column=0, columnspan=1)

        self.exit_button = tk.Button(self.root, text="❌ Çıkış", command=self.root.quit)
        self.exit_button.grid(row=7, column=2, columnspan=1)

        self.open_encrypted_button = tk.Button(self.root, text="🔓 Şifreli Yedek Aç", command=self.open_encrypted_backup)
        self.open_encrypted_button.grid(row=8, column=0, columnspan=3)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)

    def browse_backup(self):
        folder = filedialog.askdirectory()
        if folder:
            self.backup_entry.delete(0, tk.END)
            self.backup_entry.insert(0, folder)

    def get_next_backup_name(self):
        existing = [f for f in os.listdir(self.backup_dir) if f.startswith("yedek") and f.endswith(".zip")]
        numbers = []
        for f in existing:
            try:
                num = int(f.replace("yedek", "").replace(".zip", ""))
                numbers.append(num)
            except:
                continue
        next_num = max(numbers, default=0) + 1
        return f"yedek{next_num}.zip"

    def start_backup_thread(self):
        thread = threading.Thread(target=self.perform_backup)
        thread.start()

    def perform_backup(self):
        self.source_dir = self.source_entry.get()
        self.backup_dir = self.backup_entry.get()
        self.password = self.password_entry.get()

        if not all([self.source_dir, self.backup_dir, self.password]):
            messagebox.showerror("Eksik Bilgi", "Klasör ve şifre bilgileri eksik.")
            return

        self.backup_button.config(state=tk.DISABLED)
        self.status_label.config(text="⏳ Yedekleniyor...", fg="orange")

        try:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_name = self.get_next_backup_name()
            zip_path = os.path.join(self.backup_dir, zip_name)
            files_backed_up = []

            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(self.password.encode())

                for root_dir, _, files in os.walk(self.source_dir):
                    for file in files:
                        full_path = os.path.join(root_dir, file)
                        rel_path = os.path.relpath(full_path, self.source_dir)
                        zf.write(full_path, arcname=rel_path)
                        files_backed_up.append(rel_path)

            report = self.generate_report(zip_name, files_backed_up)
            report_path = os.path.join(self.backup_dir, f"rapor_{now}.txt")
            with open(report_path, 'w') as f:
                f.write(report)

            self.backup_history.append(zip_path)
            self.save_backup_history()

            self.status_label.config(text=f"✅ Yedek tamamlandı: {zip_name}", fg="green")
            messagebox.showinfo("Başarılı", f"Yedekleme tamamlandı: {zip_name}")

        except Exception as e:
            self.status_label.config(text="❌ Hata oluştu", fg="red")
            messagebox.showerror("Hata", str(e))

        self.backup_button.config(state=tk.NORMAL)

    def generate_report(self, zip_name, files):
        report = f"Yedek Adı: {zip_name}\n"
        report += f"Toplam Dosya: {len(files)}\n"
        report += "Dosyalar:\n"
        for file in files:
            report += f" - {file}\n"
        return report

    def show_previous_backups(self):
        if not self.backup_history:
            messagebox.showinfo("Yedek Geçmişi", "Hiç yedek alınmamış.")
        else:
            info = "Önceki Yedekler:\n" + "\n".join(self.backup_history)
            messagebox.showinfo("Yedek Geçmişi", info)

    def delete_previous_backups(self):
        if not self.backup_history:
            messagebox.showinfo("Yedek Geçmişi", "Silinecek yedek bulunmuyor.")
            return

        response = messagebox.askyesno("Yedekleri Sil", "Yedek dosyalarını silmek istediğinizden emin misiniz?")
        if response:
            for backup in self.backup_history[:]:
                try:
                    os.remove(backup)
                    self.backup_history.remove(backup)
                except Exception as e:
                    messagebox.showerror("Hata", f"Yedek silinemedi: {str(e)}")
                    continue
            self.save_backup_history()
            messagebox.showinfo("Başarılı", "Yedekler başarıyla silindi.")
            self.status_label.config(text="Durum: Hazır", fg="black")
        else:
            messagebox.showinfo("İptal Edildi", "Yedek silme işlemi iptal edildi.")

    def open_encrypted_backup(self):
        backup_path = filedialog.askopenfilename(title="Şifreli Yedek Dosyasını Seç", filetypes=[("ZIP Files", "*.zip")])
        if not backup_path:
            return

        entered_password = self.ask_for_password()
        if not entered_password:
            return

        try:
            with pyzipper.AESZipFile(backup_path) as zf:
                zf.setpassword(entered_password.encode())
                zf.testzip()  # Şifreyi doğrula

                # Zip içeriğini konsola yazdır (isteğe bağlı)
                print("Zip içeriği:")
                for f in zf.namelist():
                    print(f)

                extract_dir = filedialog.askdirectory(title="Yedeği Açmak İçin Klasör Seç")
                if not extract_dir:
                    messagebox.showinfo("İptal", "Açma işlemi iptal edildi.")
                    return

                zf.extractall(path=extract_dir)

            messagebox.showinfo("Başarılı", f"Yedek başarıyla açıldı ve şu klasöre çıkarıldı:\n\n{extract_dir}\n\nDosyaları bu klasörde kontrol ediniz.")

            # Windows için klasörü açmak isterseniz:
            if os.name == 'nt':
                os.startfile(extract_dir)
            # MacOS için:
            elif os.uname().sysname == 'Darwin':
                os.system(f'open "{extract_dir}"')
            # Linux için:
            else:
                os.system(f'xdg-open "{extract_dir}"')

        except RuntimeError:
            messagebox.showerror("Hata", "Şifre yanlış veya dosya açılamıyor.")
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmedik hata: {str(e)}")

    def ask_for_password(self):
        pwd_win = tk.Toplevel(self.root)
        pwd_win.title("Yedek Şifresi Giriniz")

        tk.Label(pwd_win, text="Şifre:").grid(row=0, column=0)
        pwd_entry = tk.Entry(pwd_win, show="*")
        pwd_entry.grid(row=0, column=1)

        password = []

        def submit():
            password.append(pwd_entry.get())
            pwd_win.destroy()

        tk.Button(pwd_win, text="Gönder", command=submit).grid(row=1, column=0, columnspan=2)

        pwd_win.grab_set()
        self.root.wait_window(pwd_win)

        return password[0] if password else None

    def clear_fields(self):
        self.source_entry.delete(0, tk.END)
        self.backup_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="Durum: Hazır", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
