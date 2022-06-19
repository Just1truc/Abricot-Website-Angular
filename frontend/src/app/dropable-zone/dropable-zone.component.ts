import { Component, OnInit, Input, Output, EventEmitter, HostListener } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { faUpload } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-dropable-zone',
  templateUrl: './dropable-zone.component.html',
  styleUrls: ['./dropable-zone.component.scss']
})
export class DropableZoneComponent implements OnInit {

  @Output() dropValueEvent = new EventEmitter<FileList>();

  uploadIcon = faUpload;

  @HostListener('dragover', ['$event'])
  onDragOver(event: any) {
    event.preventDefault();
  }

  @HostListener('drop', ['$event'])
  onDrop(event: any) {
    event.preventDefault();
    this.dropValueEvent.emit(event.dataTransfer.files);
  }

  constructor(private toastr: ToastrService) { }

  onChange(event: any) {
    this.dropValueEvent.emit(event.target.files);
  }

  ngOnInit(): void {
  }

}
