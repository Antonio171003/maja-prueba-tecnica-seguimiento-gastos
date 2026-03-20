import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Expense, ExpenseFilters, ExpensePage } from '../models/expense.model';

@Injectable({ providedIn: 'root' })
export class ExpenseService {
  private http = inject(HttpClient);
  private url = '/expenses';

  getAll(filters: ExpenseFilters = {}): Observable<ExpensePage> {
    let params = new HttpParams();
    Object.entries(filters).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        params = params.set(key, String(val));
      }
    });
    return this.http.get<ExpensePage>(this.url, { params });
  }

  create(data: Omit<Expense, 'id' | 'created_at'>): Observable<Expense> {
    return this.http.post<Expense>(this.url, data);
  }

  update(id: number, data: Partial<Expense>): Observable<Expense> {
    return this.http.put<Expense>(`${this.url}/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
