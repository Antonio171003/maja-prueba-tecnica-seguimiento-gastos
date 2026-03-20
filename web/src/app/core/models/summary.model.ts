export interface CategorySummary {
  category_id: number;
  category_name: string;
  count: number;
  total: number;
}

export interface Summary {
  total: number;
  count: number;
  by_category: CategorySummary[];
}