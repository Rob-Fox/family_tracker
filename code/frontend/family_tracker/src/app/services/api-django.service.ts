import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiDjangoService {

  constructor(private http:HttpClient) {
    this.http.get(myUrl).subscribe((response) => {
      console.log(response)
    })
  }
}
