import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'app/expenses',
    pathMatch: 'full'
  },
  {
    path: 'app/expenses',
    loadComponent: () =>
      import('./features/expenses/expense-list/expense-list')
        .then(m => m.ExpenseList)
  },
  {
    path: 'app/summary',
    loadComponent: () =>
      import('./features/summary/summary')
        .then(m => m.Summary)
  }
];