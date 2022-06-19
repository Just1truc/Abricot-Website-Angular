import { Component, Input, OnInit } from '@angular/core';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal';
import { ModalComponent } from '../modal/modal.component';
import { LevelCardModel } from '../models/level-card.model';

@Component({
  selector: 'app-level-card',
  templateUrl: './level-card.component.html',
  styleUrls: ['./level-card.component.scss']
})
export class LevelCardComponent implements OnInit {

  hover: boolean = false;
  @Input() level!: LevelCardModel;

  modalRef!: MdbModalRef<ModalComponent> | null;

  openMd() {
    this.modalRef = this.modalService.open(ModalComponent,
      {
        data :
        {
          cardData : this.level
        }
      });
  }

  constructor(private modalService : MdbModalService) { }

  ngOnInit(): void {
    this.modalRef = null;
  }

}
