import { Component, OnInit, Input } from '@angular/core';
import { ColoredSpaceModel } from '../models/colored-space.model';

@Component({
  selector: 'app-colored-space',
  templateUrl: './colored-space.component.html',
  styleUrls: ['./colored-space.component.scss']
})
export class ColoredSpaceComponent implements OnInit {

  @Input() model!: ColoredSpaceModel;

  constructor() { }

  ngOnInit(): void {
  }

}
