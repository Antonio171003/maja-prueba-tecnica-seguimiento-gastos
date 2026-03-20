import { Component, inject } from '@angular/core';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';
import { CategoryService } from '../../../core/services/category.service';

@Component({
  selector: 'app-category-form',
  imports: [
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    FormsModule,
  ],
  templateUrl: './category-form.html',
  styleUrl: './category-form.scss',
})
export class CategoryForm {
  private categoryService = inject(CategoryService);
  private dialogRef = inject(MatDialogRef<CategoryForm>);

  name = '';
  loading = false;
  error: string | null = null;

  isValid(): boolean {
    return this.name.trim().length > 0;
  }

  submit() {
    if (!this.isValid()) return;

    this.loading = true;
    this.error = null;

    this.categoryService.create(this.name.trim()).subscribe({
      next: () => this.dialogRef.close(true),
      error: (err) => {
        this.error = err?.error?.error ?? 'Error al crear la categoría';
        this.loading = false;
      }
    });
  }

  cancel() {
    this.dialogRef.close(false);
  }
}