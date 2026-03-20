import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Summary } from '../models/summary.model';

@Injectable({ providedIn: 'root' })
export class SummaryService {
  private http = inject(HttpClient);
  private url = '/expenses/summary';

  get(filters: { category_id?: number; start_date?: string; end_date?: string } = {}): Observable<Summary> {
    let params = new HttpParams();
    Object.entries(filters).forEach(([key, val]) => {
      if (val !== undefined && val !== '') {
        params = params.set(key, String(val));
      }
    });
    return this.http.get<Summary>(this.url, { params });
  }
}
