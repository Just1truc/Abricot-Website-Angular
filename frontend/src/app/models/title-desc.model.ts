import { CssSelector } from "@angular/compiler";

export class TitleDescModel {
    title!:string;
    desc!:string;
    font!:string;
    constructor(title:string, desc:string, font:string) {
        this.title = title;
        this.desc = desc;
        this.font = font;
    }
}