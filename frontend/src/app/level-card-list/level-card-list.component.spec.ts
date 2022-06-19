import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LevelCardListComponent } from './level-card-list.component';

describe('LevelCardListComponent', () => {
  let component: LevelCardListComponent;
  let fixture: ComponentFixture<LevelCardListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LevelCardListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LevelCardListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
