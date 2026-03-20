import { Component, input, output, inject, OnInit, signal } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { FormsModule } from '@angular/forms';
import { Category } from '../../../core/models/category.model';
import { ExpenseFilters } from '../../../core/models/expense.model';

@Component({
  selector: 'app-expense-filters',
  imports: [
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    FormsModule,
  ],
  templateUrl: './expense-filters.html',
  styleUrl: './expense-filters.scss',
})
export class ExpenseFiltersComponent {
  categories = input<Category[]>([]);
  filtersChange = output<ExpenseFilters>();

  categoryId: number | null = null;
  startDate = '';
  endDate = '';
  minAmount: number | null = null;
  maxAmount: number | null = null;
  sort: ExpenseFilters['sort'] = 'date_desc';

  sortOptions = [
    { value: 'date_desc',   label: 'Fecha (más reciente)' },
    { value: 'date_asc',    label: 'Fecha (más antigua)'  },
    { value: 'amount_desc', label: 'Monto (mayor)'        },
    { value: 'amount_asc',  label: 'Monto (menor)'        },
  ];

  apply() {
    const filters: ExpenseFilters = { sort: this.sort };
    if (this.categoryId)  filters.category_id = this.categoryId;
    if (this.startDate)   filters.start_date  = this.startDate;
    if (this.endDate)     filters.end_date    = this.endDate;
    if (this.minAmount)   filters.min_amount  = this.minAmount;
    if (this.maxAmount)   filters.max_amount  = this.maxAmount;
    this.filtersChange.emit(filters);
  }

  reset() {
    this.categoryId = null;
    this.startDate  = '';
    this.endDate    = '';
    this.minAmount  = null;
    this.maxAmount  = null;
    this.sort       = 'date_desc';
    this.filtersChange.emit({ sort: 'date_desc' });
  }
}