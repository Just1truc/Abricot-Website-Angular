import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  constructor (private router: ActivatedRoute) {}

  ngOnInit(): void {
  }

  openLink(url : string) {
    window.location.href = url;
  }

}
