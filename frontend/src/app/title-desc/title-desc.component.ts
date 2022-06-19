import { Component, Input, OnInit } from '@angular/core';
import { TitleDescModel } from '../models/title-desc.model';

@Component({
  selector: 'app-title-desc',
  templateUrl: './title-desc.component.html',
  styleUrls: ['./title-desc.component.scss']
})
export class TitleDescComponent implements OnInit {

  @Input() model!: TitleDescModel;

  constructor() { }

  ngOnInit(): void {
  }

}
