export class ColoredSpaceModel {
    txtColor!:string;
    bgColor!:string;
    padding!:string;
    height!:string;
    constructor(txtColor:string, bgColor:string, padding:string, height:string) {
        this.txtColor = txtColor;
        this.bgColor = bgColor;
        this.padding = padding;
        this.height = height;
    }
}