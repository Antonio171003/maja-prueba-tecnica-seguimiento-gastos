export interface Expense {
  id: number;
  amount: number;
  description: string;
  date: string;
  category_id: number;
  created_at?: string;
}

export interface ExpenseFilters {
  category_id?: number;
  start_date?: string;
  end_date?: string;
  min_amount?: number;
  max_amount?: number;
  sort?: 'date_asc' | 'date_desc' | 'amount_asc' | 'amount_desc';
  page?: number;
  limit?: number;
}

export interface ExpensePage {
  data: Expense[];
  total: number;
  page: number;
  pages: number;
  limit: number;
}
