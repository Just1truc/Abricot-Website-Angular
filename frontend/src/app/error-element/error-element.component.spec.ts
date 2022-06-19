import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorElementComponent } from './error-element.component';

describe('ErrorElementComponent', () => {
  let component: ErrorElementComponent;
  let fixture: ComponentFixture<ErrorElementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ErrorElementComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ErrorElementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
