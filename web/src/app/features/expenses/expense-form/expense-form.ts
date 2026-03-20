import { Component, inject, OnInit } from '@angular/core';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';
import { ExpenseService } from '../../../core/services/expense.service';
import { Category } from '../../../core/models/category.model';
import { Expense } from '../../../core/models/expense.model';

@Component({
  selector: 'app-expense-form',
  imports: [
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    FormsModule,
  ],
  templateUrl: './expense-form.html',
  styleUrl: './expense-form.scss',
})
export class ExpenseForm implements OnInit {
  private expenseService = inject(ExpenseService);
  private dialogRef = inject(MatDialogRef<ExpenseForm>);
  data = inject<{ expense?: Expense; categories: Category[] }>(MAT_DIALOG_DATA);

  isEdit = false;
  loading = false;
  error: string | null = null;

  form = {
    amount: null as number | null,
    description: '',
    date: '',
    category_id: null as number | null,
  };

  ngOnInit() {
    if (this.data?.expense) {
      this.isEdit = true;
      const e = this.data.expense;
      this.form = {
        amount:      e.amount,
        description: e.description,
        date:        e.date,
        category_id: e.category_id,
      };
    }
  }

  get categories() {
    return this.data?.categories ?? [];
  }

  isValid(): boolean {
    return !!(
      this.form.amount &&
      this.form.amount > 0 &&
      this.form.date &&
      this.form.category_id
    );
  }

  submit() {
    if (!this.isValid()) return;

    this.loading = true;
    this.error = null;

    const payload = {
      amount:      this.form.amount!,
      description: this.form.description,
      date:        this.form.date,
      category_id: this.form.category_id!,
    };

    const request$ = this.isEdit
      ? this.expenseService.update(this.data.expense!.id, payload)
      : this.expenseService.create(payload);

    request$.subscribe({
      next: () => this.dialogRef.close(true),
      error: (err) => {
        this.error = err?.error?.errors?.join(', ') ?? 'Error al guardar el gasto';
        this.loading = false;
      }
    });
  }

  cancel() {
    this.dialogRef.close(false);
  }
}