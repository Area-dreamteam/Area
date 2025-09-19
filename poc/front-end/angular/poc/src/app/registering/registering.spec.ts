import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Registering } from './registering';

describe('Registering', () => {
  let component: Registering;
  let fixture: ComponentFixture<Registering>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Registering]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Registering);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
