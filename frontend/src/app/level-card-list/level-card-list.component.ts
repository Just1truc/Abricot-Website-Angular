import { Component, OnInit } from '@angular/core';
import { OutputCardService } from '../services/output-card.service';
import { LevelCardModel } from '../models/level-card.model';

@Component({
  selector: 'app-level-card-list',
  templateUrl: './level-card-list.component.html',
  styleUrls: ['./level-card-list.component.scss']
})
export class LevelCardListComponent implements OnInit {

  cards: LevelCardModel[];

  constructor(private cardService: OutputCardService) {
    this.cards = this.cardService.levelCards;
  }

  ngOnInit(): void {
  }

}
