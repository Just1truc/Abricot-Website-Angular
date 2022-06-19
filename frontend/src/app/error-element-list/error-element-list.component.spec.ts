import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorElementListComponent } from './error-element-list.component';

describe('ErrorElementListComponent', () => {
  let component: ErrorElementListComponent;
  let fixture: ComponentFixture<ErrorElementListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ErrorElementListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ErrorElementListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
