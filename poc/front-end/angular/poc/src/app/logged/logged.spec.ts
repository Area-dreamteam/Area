import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Logged } from './logged';

describe('Logged', () => {
  let component: Logged;
  let fixture: ComponentFixture<Logged>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Logged]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Logged);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
