import { Component } from '@angular/core';
import { MdbModalRef } from 'mdb-angular-ui-kit/modal';
import { LevelCardModel } from '../models/level-card.model';
import { OnInit } from '@angular/core';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
})
export class ModalComponent {
  cardData!:LevelCardModel;

  constructor(public modalRef: MdbModalRef<ModalComponent>) {}
}
