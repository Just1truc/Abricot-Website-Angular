import { Component, Input, OnInit } from '@angular/core';
import { LevelCardModel } from '../models/level-card.model';

@Component({
  selector: 'app-error-element-list',
  templateUrl: './error-element-list.component.html',
  styleUrls: ['./error-element-list.component.scss']
})
export class ErrorElementListComponent implements OnInit {

  @Input() ErrorObjects !: LevelCardModel;
  errorArray:any[] = [];

  constructor() { }

  ngOnInit() {
    for (let obj in this.ErrorObjects.list) {
      this.errorArray.push(
        {
          name : obj,
          description : this.ErrorObjects.list[obj].description,
          list : this.ErrorObjects.list[obj].list
        }
      );
    }
  }

}
