import { Injectable } from "@angular/core";
import { LevelCardModel } from "../models/level-card.model";

@Injectable({
    providedIn: "root"
})
export class OutputCardService {
    levelCards: LevelCardModel[] = [
        new LevelCardModel(
        "MAJOR",
        0,
        "#E2423E",
        "white"
    ),
    new LevelCardModel(
        "MINOR",
        0,
        "#F6DC32",
        "white"
    ),
    new LevelCardModel(
        "INFO",
        0,
        "#94CDDD",
        "white"
    )
    ];


}