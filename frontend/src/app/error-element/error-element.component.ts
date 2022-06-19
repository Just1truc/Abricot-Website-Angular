import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-error-element',
  templateUrl: './error-element.component.html',
  styleUrls: ['./error-element.component.scss']
})
export class ErrorElementComponent implements OnInit {

  @Input() errorObject !:
  {
    name : string,
    description : string,
    list : {file:string, line:string}[]
  };

  constructor() { }

  ngOnInit(): void {
    this.errorObject.list.forEach(element => {
      element.file = element.file.slice(element.file.indexOf("/") + 1)
    });
  }

}
