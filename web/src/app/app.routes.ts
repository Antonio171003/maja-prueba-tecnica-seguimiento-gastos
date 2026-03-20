import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'expenses',
    pathMatch: 'full'
  },
  {
    path: 'expenses',
    loadComponent: () =>
      import('./features/expenses/expense-list/expense-list')
        .then(m => m.ExpenseList)
  },
  {
    path: 'summary',
    loadComponent: () =>
      import('./features/summary/summary')
        .then(m => m.Summary)
  }
];