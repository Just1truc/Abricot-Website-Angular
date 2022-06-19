import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LevelCardComponent } from './level-card.component';

describe('LevelCardComponent', () => {
  let component: LevelCardComponent;
  let fixture: ComponentFixture<LevelCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LevelCardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LevelCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
