import flet as ft, time, traceback, os

class Operation(ft.UserControl):
    
    def build(self):
                        
        self.close_button = ft.TextButton("Close", disabled=True, on_click=self.close_dialog)

        self.loading = ft.ProgressRing(value=None, width=60, height=60, stroke_width=5, bgcolor=ft.colors.GREY, color=ft.colors.WHITE)
        
        self.tracker = ft.Text(text_align=ft.TextAlign.CENTER)

        self.modal_dialog = ft.AlertDialog(
            title=self.tracker,
            content=ft.Container(
                content=self.loading, 
                alignment=ft.alignment.center, height=100, width=100
            ),
            content_padding=30, modal=True, 
            actions=[self.close_button], actions_alignment=ft.MainAxisAlignment.CENTER
        )

        return self.modal_dialog


    def _after_operations(self): #Enable UI after operation is successful
        self.close_button.disabled = False
        self.tracker.value = self.tracker.value + ' Finished'
        self.update()

    def check_if_backup_exists(self, folder):
        '''
        Temporary (Need to find a better solution):
        Checks if the selected folder is a new backup or already contains a previous backup.

        pymobiledevice's info function has some issue, thus this func exists as an alternative.
        '''
        files = os.listdir(folder)

        if len(files) == 0:
            return False #Fresh backup folder
        else:
            get_backup_files = files[0]
            if 'Info.plist' in get_backup_files:
                return True# A backup exists
            else:
                return False


    def backup(self, folder, pwd, service, is_first_backup):

        self.modal_dialog.open = True
        self.tracker.value = "Backing Up"
        self.update()

        #run process
        try:
            service.backup(
                backup_directory=folder,
                progress_callback=self.progressbar,
                full=True
            )
        except:
            print(traceback.format_exc())
            self.close_dialog()
            return False
        else:
            self._after_operations()
            return True
    
    def restore(self, folder, pwd, service, identifier):

        self.modal_dialog.open = True
        self.tracker.value = "Backing Up"
        self.update()

        #run process
        try:
            service.restore(
                backup_directory=folder,
                progress_callback=self.progressbar,
                password=pwd,
                source=identifier
            )
        except:
            print(traceback.format_exc())
            self.close_dialog()
            return False
        else:
            self._after_operations()
            return True


    def close_dialog(self, e=None):

        #Reset properties to default
        self.close_button.disabled = True
        self.loading.value = None
        self.modal_dialog.open = False
        self.update()

    def progressbar(self, e):
        print(e)
        self.loading.value = round(e)/100
        self.loading.update()