export class LevelCardModel {
    level: string;
    numberOferrors: number;
    cardColor: string;
    textColor: string;
    list: any;
    constructor (level: string, numberOferrors: number, cardColor: string, textColor: string) {
        this.level = level;
        this.numberOferrors = numberOferrors;
        this.cardColor = cardColor;
        this.textColor = textColor;
        this.list = {};
    }
}