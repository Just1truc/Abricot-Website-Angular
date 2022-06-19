import { Component, OnInit } from '@angular/core';
import { ColoredSpaceModel } from '../models/colored-space.model';
import { TitleDescModel } from '../models/title-desc.model';
import { faGithub, IconDefinition } from '@fortawesome/free-brands-svg-icons';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements OnInit {

  coloredSpace!:ColoredSpaceModel;
  whiteSpace!:ColoredSpaceModel;
  explicationBox!:TitleDescModel;
  iconGithub:IconDefinition = faGithub;

  constructor(private router: ActivatedRoute) {}

  ngOnInit(): void {
    this.whiteSpace = new ColoredSpaceModel(
      'black',
      'transparent',
      '20px',
      'auto'
    );
    this.coloredSpace =
      new ColoredSpaceModel(
        'white',
        '#729EA1',
        '20px',
        'auto'
      );
    this.explicationBox =
      new TitleDescModel(
        'Abricot-norminette',
        'Abricot norminette is a tool to help you organize your code. It\'ll show you the error you make when structuring your code. Following it\'s recommendations, your code will be more readable and easier to maintain.',
        'sans-serif'
      );
  }

  loadLink(url: string) {
    window.location.href = url;
  }

}
