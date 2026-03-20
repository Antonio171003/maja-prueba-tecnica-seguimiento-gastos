import { Component, inject, OnInit, signal } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { CurrencyPipe, DatePipe } from '@angular/common';
import { ExpenseService } from '../../../core/services/expense.service';
import { CategoryService } from '../../../core/services/category.service';
import { Expense, ExpenseFilters, ExpensePage } from '../../../core/models/expense.model';
import { Category } from '../../../core/models/category.model';
import { ExpenseFiltersComponent } from '../expense-filters/expense-filters';import { ExpenseForm as ExpenseFormComponent } from '../expense-form/expense-form';
import { CategoryForm as CategoryFormComponent } from '../../categories/category-form/category-form';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-expense-list',
  imports: [
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatTooltipModule,
    MatPaginatorModule,
    MatCardModule,
    CurrencyPipe,
    DatePipe,
    ExpenseFiltersComponent,
  ],
  templateUrl: './expense-list.html',
  styleUrl: './expense-list.scss'
})
export class ExpenseList implements OnInit {
  private expenseService = inject(ExpenseService);
  private categoryService = inject(CategoryService);
  private dialog = inject(MatDialog);

  expenses = signal<Expense[]>([]);
  categories = signal<Category[]>([]);
  loading = signal(false);
  error = signal<string | null>(null);

  totalItems = signal(0);
  currentPage = signal(0);
  pageSize = signal(10);
  currentFilters = signal<ExpenseFilters>({});

  displayedColumns = ['date', 'description', 'category', 'amount', 'actions'];

  ngOnInit() {
    this.loadCategories();
    this.loadExpenses();
  }

  loadCategories() {
    this.categoryService.getAll().subscribe({
      next: cats => this.categories.set(cats),
      error: () => this.error.set('Error cargando categorías')
    });
  }

  loadExpenses() {
    this.loading.set(true);
    this.error.set(null);

    const filters: ExpenseFilters = {
      ...this.currentFilters(),
      page: this.currentPage() + 1,
      limit: this.pageSize(),
    };

    this.expenseService.getAll(filters).subscribe({
      next: (res: ExpensePage) => {
        this.expenses.set(res.data);
        this.totalItems.set(res.total);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Error cargando gastos');
        this.loading.set(false);
      }
    });
  }

  onFiltersChange(filters: ExpenseFilters) {
    this.currentFilters.set(filters);
    this.currentPage.set(0);
    this.loadExpenses();
  }

  onPageChange(event: PageEvent) {
    this.currentPage.set(event.pageIndex);
    this.pageSize.set(event.pageSize);
    this.loadExpenses();
  }

  getCategoryName(id: number): string {
    return this.categories().find(c => c.id === id)?.name ?? '—';
  }

  openExpenseForm(expense?: Expense) {
    const ref = this.dialog.open(ExpenseFormComponent, {
      width: '480px',
      data: { expense, categories: this.categories() }
    });
    ref.afterClosed().subscribe(result => {
      if (result) this.loadExpenses();
    });
  }

  openCategoryForm() {
    const ref = this.dialog.open(CategoryFormComponent, {
      width: '400px'
    });
    ref.afterClosed().subscribe(result => {
      if (result) this.loadCategories();
    });
  }

  deleteExpense(id: number) {
    if (!confirm('¿Eliminar este gasto?')) return;
    this.expenseService.delete(id).subscribe({
      next: () => this.loadExpenses(),
      error: () => this.error.set('Error eliminando gasto')
    });
  }
}