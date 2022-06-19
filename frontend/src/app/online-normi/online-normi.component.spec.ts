import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnlineNormiComponent } from './online-normi.component';

describe('OnlineNormiComponent', () => {
  let component: OnlineNormiComponent;
  let fixture: ComponentFixture<OnlineNormiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OnlineNormiComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OnlineNormiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
