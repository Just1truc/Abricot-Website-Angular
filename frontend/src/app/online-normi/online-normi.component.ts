import { Component, OnInit, HostListener } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { OutputCardService } from '../services/output-card.service';
import { LevelCardModel } from '../models/level-card.model';

@Component({
  selector: 'app-online-normi',
  templateUrl: './online-normi.component.html',
  styleUrls: ['./online-normi.component.scss']
})
export class OnlineNormiComponent implements OnInit {

  selectedFolder!: File;
  folderName!: string;
  formData!:FormData;
  outputStatus!:boolean;
  buttonStatus!:boolean;

  baseApiUrl = "https://gallant-brattain.51-38-225-77.plesk.page/check-norme";

  constructor(
    private http: HttpClient,
    private toastr: ToastrService,
    private outputService : OutputCardService) { }

  ngOnInit(): void {
      this.outputStatus = false;
      this.buttonStatus = false;
  }

  onStart(): void {
    if (this.folderName && this.selectedFolder) {
      this.toastr.success('Started norminette', 'Norminette started', {
        timeOut: 3000,
        progressBar: true,
        closeButton: true
      });
      // launch norminette
      this.onFileSelected(this.selectedFolder);
    } else {
      this.toastr.error('No folder selected', 'Error', {
        timeOut: 3000,
        progressBar: true,
        closeButton: true
      });
    }
  }

  dropFunction (event: FileList): void {
    if (event.length > 1) {
      this.toastr.error('Only one file can be upload', 'Error', {
        timeOut: 3000,
        progressBar: true,
        closeButton: true
      });
      return;
    } else if (event[0].type !== "application/x-tar") {
      this.toastr.error('Only tar files can be upload', 'Error', {
        timeOut: 3000,
        progressBar: true,
        closeButton: true
      });
      return;
    }
    this.toastr.success('File uploaded', 'Success', {
      timeOut: 3000,
      progressBar: true,
      closeButton: true
    });
    this.selectedFolder = event[0];
    this.folderName = this.selectedFolder.name;
    this.formData = new FormData();
    this.formData.append("file", this.selectedFolder, this.folderName);
  }

  onFileSelected(file: File) {
    if (file) {
        this.buttonStatus = true;
        this.outputStatus = true;
        this.http.post(this.baseApiUrl, this.formData, {
          reportProgress: true,
          observe: 'events'
        })
        .subscribe((result: any) => {
          if (result.body) {
            result.body = JSON.parse(result.body);
            console.log(result.body);
            this.outputService.levelCards.forEach((card : LevelCardModel) => {
              card.numberOferrors = result.body[card.level.toLowerCase()].count;
              card.list = result.body[card.level.toLowerCase()].list;
            })
            this.toastr.success('Norminette finished', 'Norminette finished', {
              timeOut: 3000,
              progressBar: true,
              closeButton: true
            });
            this.outputStatus = false;
            this.buttonStatus = false;
          }
        },
        () => {
          this.toastr.error("Backend server can't be reached", 'Error');
          this.outputStatus = false;
          this.buttonStatus = false;
        })
    }
}
}
