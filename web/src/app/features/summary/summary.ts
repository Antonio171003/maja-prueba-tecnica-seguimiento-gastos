import { Component, inject, OnInit, signal } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { CurrencyPipe } from '@angular/common';
import { SummaryService } from '../../core/services/summary.service';
import { CategoryService } from '../../core/services/category.service';
import { Summary as SummaryData, CategorySummary } from '../../core/models/summary.model';
import { Category } from '../../core/models/category.model';

@Component({
  selector: 'app-summary',
  imports: [
    MatCardModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatTableModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    FormsModule,
    CurrencyPipe,
  ],
  templateUrl: './summary.html',
  styleUrl: './summary.scss',
})
export class Summary implements OnInit {
  private summaryService = inject(SummaryService);
  private categoryService = inject(CategoryService);

  summary = signal<SummaryData | null>(null);
  categories = signal<Category[]>([]);
  loading = signal(false);
  error = signal<string | null>(null);

  categoryId: number | null = null;
  startDate = '';
  endDate = '';

  displayedColumns = ['category', 'count', 'total', 'percent'];

  ngOnInit() {
    this.categoryService.getAll().subscribe({
      next: cats => this.categories.set(cats)
    });
    this.load();
  }

  load() {
    this.loading.set(true);
    this.error.set(null);

    const filters: any = {};
    if (this.categoryId) filters.category_id = this.categoryId;
    if (this.startDate)  filters.start_date  = this.startDate;
    if (this.endDate)    filters.end_date    = this.endDate;

    this.summaryService.get(filters).subscribe({
      next: (data: SummaryData) => {
        this.summary.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Error cargando el resumen');
        this.loading.set(false);
      }
    });
  }

  reset() {
    this.categoryId = null;
    this.startDate  = '';
    this.endDate    = '';
    this.load();
  }

  getPercent(row: CategorySummary): number {
    const total = this.summary()?.total ?? 0;
    if (total === 0) return 0;
    return Math.round((row.total / total) * 100);
  }
}