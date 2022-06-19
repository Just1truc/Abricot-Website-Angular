import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ColoredSpaceComponent } from './colored-space.component';

describe('ColoredSpaceComponent', () => {
  let component: ColoredSpaceComponent;
  let fixture: ComponentFixture<ColoredSpaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ColoredSpaceComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ColoredSpaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
