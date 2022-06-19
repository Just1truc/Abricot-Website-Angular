import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TitleDescComponent } from './title-desc.component';

describe('TitleDescComponent', () => {
  let component: TitleDescComponent;
  let fixture: ComponentFixture<TitleDescComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TitleDescComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TitleDescComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
