import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DropableZoneComponent } from './dropable-zone.component';

describe('DropableZoneComponent', () => {
  let component: DropableZoneComponent;
  let fixture: ComponentFixture<DropableZoneComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DropableZoneComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DropableZoneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
