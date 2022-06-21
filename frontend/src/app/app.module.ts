import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ColoredSpaceComponent } from './colored-space/colored-space.component';
import { MainPageComponent } from './main-page/main-page.component';
import { TitleDescComponent } from './title-desc/title-desc.component';
import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { ContactComponent } from './contact/contact.component';
import { OnlineNormiComponent } from './online-normi/online-normi.component';
import { LevelCardComponent } from './level-card/level-card.component';
import { LevelCardListComponent } from './level-card-list/level-card-list.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';
import { DropableZoneComponent } from './dropable-zone/dropable-zone.component';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ModalComponent } from './modal/modal.component';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { MdbModalModule } from 'mdb-angular-ui-kit/modal';
import { ErrorElementComponent } from './error-element/error-element.component';
import { ErrorElementListComponent } from './error-element-list/error-element-list.component';
import { NgxSpinnerModule } from 'ngx-spinner';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ColoredSpaceComponent,
    MainPageComponent,
    TitleDescComponent,
    ContactComponent,
    OnlineNormiComponent,
    LevelCardComponent,
    LevelCardListComponent,
    DropableZoneComponent,
    ModalComponent,
    ErrorElementComponent,
    ErrorElementListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CommonModule,
    FontAwesomeModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MDBBootstrapModule,
    MdbModalModule,
    NgxSpinnerModule,
    MatProgressSpinnerModule,
    ToastrModule.forRoot({
      positionClass: 'toast-bottom-right',
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
