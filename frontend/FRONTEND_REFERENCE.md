# Money Tracker - Frontend Reference (Nuxt.js)

**Version:** 1.0  
**Last Updated:** 2025-10-25  
**Technology:** Nuxt.js 3 + Vue 3 + TypeScript

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Type Definitions](#type-definitions)
5. [API Integration](#api-integration)
6. [State Management](#state-management)
7. [Components](#components)
8. [Pages & Routing](#pages--routing)
9. [Utilities](#utilities)
10. [Development Guidelines](#development-guidelines)
11. [Testing](#testing)
12. [Deployment](#deployment)

---

## Project Overview

### Purpose
Frontend application for Money Tracker - a personal finance tracking system that communicates with a FastAPI backend to manage transactions, budgets, and financial analytics.

### Key Features
- ✅ User authentication (JWT-based)
- ✅ Dashboard with financial overview
- ✅ Transaction management (CRUD)
- ✅ Multiple account tracking
- ✅ Category management
- ✅ Budget creation and tracking
- ✅ Analytics and reports
- ✅ Responsive design
- 🔄 PDF statement upload (future)

### Design Principles
1. **Type Safety**: Full TypeScript coverage
2. **Composition API**: Use Vue 3 Composition API
3. **Reusable Composables**: Extract logic to composables
4. **Component-Based**: Modular, reusable components
5. **User Experience**: Fast, intuitive, responsive

---

## Technology Stack

### Core Framework
- **Nuxt.js**: 3.x (Vue 3, Composition API)
- **Vue**: 3.x
- **TypeScript**: 5.x

### State Management
- **Pinia**: Official state management for Vue 3
- **Composables**: For local state and logic

### HTTP Client
- **$fetch**: Built-in Nuxt fetch (or Axios as alternative)
- **ofetch**: Underlying fetch library

### UI & Styling
- **CSS Framework**: Tailwind CSS (recommended) or custom CSS
- **Icons**: Heroicons, Lucide, or Material Icons
- **Charts**: Chart.js or ApexCharts
- **Date Picker**: VueUse DatePicker or custom

### Utilities
- **Day.js**: Date manipulation
- **VeeValidate**: Form validation (optional)
- **Zod**: Schema validation (optional)

### Development Tools
- **pnpm/npm/yarn**: Package management
- **Vitest**: Unit testing
- **Playwright**: E2E testing
- **ESLint**: Code linting
- **Prettier**: Code formatting

---

## Project Structure

```
frontend/
├── .nuxt/                           # Auto-generated
├── .output/                         # Build output
│
├── assets/
│   ├── css/
│   │   ├── main.css                 # Global styles
│   │   └── variables.css            # CSS variables
│   └── icons/                       # SVG icons
│
├── components/
│   ├── common/                      # Reusable UI components
│   │   ├── AppButton.vue
│   │   ├── AppInput.vue
│   │   ├── AppSelect.vue
│   │   ├── AppDatePicker.vue
│   │   ├── AppModal.vue
│   │   ├── AppCard.vue
│   │   ├── AppTable.vue
│   │   ├── AppPagination.vue
│   │   └── AppLoading.vue
│   │
│   ├── layout/                      # Layout components
│   │   ├── TheHeader.vue
│   │   ├── TheSidebar.vue
│   │   ├── TheFooter.vue
│   │   └── BreadcrumbNav.vue
│   │
│   ├── transactions/                # Transaction components
│   │   ├── TransactionList.vue
│   │   ├── TransactionForm.vue
│   │   ├── TransactionItem.vue
│   │   ├── TransactionFilter.vue
│   │   ├── QuickAddTransaction.vue
│   │   └── BulkEditModal.vue
│   │
│   ├── accounts/                    # Account components
│   │   ├── AccountCard.vue
│   │   ├── AccountForm.vue
│   │   ├── AccountSelector.vue
│   │   └── AccountBalance.vue
│   │
│   ├── categories/                  # Category components
│   │   ├── CategoryTree.vue
│   │   ├── CategoryForm.vue
│   │   ├── CategoryIcon.vue
│   │   └── CategorySelector.vue
│   │
│   ├── budgets/                     # Budget components
│   │   ├── BudgetCard.vue
│   │   ├── BudgetForm.vue
│   │   ├── BudgetProgress.vue
│   │   └── BudgetList.vue
│   │
│   ├── analytics/                   # Analytics components
│   │   ├── SpendingChart.vue
│   │   ├── CategoryPieChart.vue
│   │   ├── TrendLineChart.vue
│   │   ├── MonthlyComparison.vue
│   │   └── StatsCard.vue
│   │
│   └── dashboard/                   # Dashboard components
│       ├── DashboardStats.vue
│       ├── RecentTransactions.vue
│       ├── SpendingOverview.vue
│       └── BudgetSummary.vue
│
├── composables/                     # Reusable logic
│   ├── useApi.ts                    # API wrapper
│   ├── useAuth.ts                   # Authentication
│   ├── useTransactions.ts           # Transaction operations
│   ├── useAccounts.ts               # Account operations
│   ├── useCategories.ts             # Category operations
│   ├── useBudgets.ts                # Budget operations
│   ├── useAnalytics.ts              # Analytics data
│   ├── useCurrency.ts               # IDR formatting
│   ├── useDate.ts                   # Date utilities
│   └── useNotification.ts           # Toast notifications
│
├── layouts/                         # Page layouts
│   ├── default.vue                  # Main layout
│   ├── auth.vue                     # Auth pages layout
│   └── empty.vue                    # Minimal layout
│
├── pages/                           # File-based routing
│   ├── index.vue                    # Dashboard
│   ├── login.vue                    # Login page
│   ├── register.vue                 # Registration
│   │
│   ├── accounts/
│   │   ├── index.vue                # Account list
│   │   ├── [id].vue                 # Account detail
│   │   └── create.vue               # Create account
│   │
│   ├── transactions/
│   │   ├── index.vue                # Transaction list
│   │   ├── [id].vue                 # Transaction detail
│   │   ├── create.vue               # Add transaction
│   │   └── edit-[id].vue            # Edit transaction
│   │
│   ├── categories/
│   │   └── index.vue                # Category management
│   │
│   ├── budgets/
│   │   ├── index.vue                # Budget list
│   │   └── [id].vue                 # Budget detail
│   │
│   ├── analytics/
│   │   ├── index.vue                # Analytics dashboard
│   │   ├── spending.vue             # Spending analysis
│   │   ├── trends.vue               # Trend analysis
│   │   └── reports.vue              # Custom reports
│   │
│   └── settings/
│       ├── index.vue                # General settings
│       ├── profile.vue              # User profile
│       └── preferences.vue          # App preferences
│
├── plugins/                         # Nuxt plugins
│   ├── api.ts                       # API client setup
│   └── dayjs.ts                     # Date library
│
├── middleware/                      # Route middleware
│   ├── auth.ts                      # Auth guard
│   └── guest.ts                     # Guest-only guard
│
├── stores/                          # Pinia stores
│   ├── auth.ts                      # Auth state
│   ├── accounts.ts                  # Account state
│   ├── transactions.ts              # Transaction state
│   ├── categories.ts                # Category state
│   ├── budgets.ts                   # Budget state
│   └── ui.ts                        # UI state
│
├── types/                           # TypeScript types
│   ├── index.ts
│   ├── auth.ts
│   ├── account.ts
│   ├── transaction.ts
│   ├── category.ts
│   ├── budget.ts
│   └── api.ts
│
├── utils/                           # Utility functions
│   ├── currency.ts                  # IDR formatting
│   ├── date.ts                      # Date formatting
│   ├── validation.ts                # Validators
│   └── constants.ts                 # App constants
│
├── .env.example
├── .env
├── nuxt.config.ts                   # Nuxt configuration
├── tsconfig.json                    # TypeScript config
├── tailwind.config.js               # Tailwind config (if using)
├── package.json
└── README.md
```

---

## Type Definitions

### Core Types

#### `types/auth.ts`
```typescript
export interface User {
  id: string
  email: string
  username: string
  full_name: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at: string
  last_login?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name: string
}

export interface AuthResponse {
  user: User
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface TokenPayload {
  sub: string
  username: string
  exp: number
  iat: number
  type: 'access' | 'refresh'
}
```

#### `types/account.ts`
```typescript
export interface Account {
  id: string
  user_id: string
  account_number?: string
  account_name: string
  bank_name: string
  account_type: string
  currency: string
  initial_balance: number
  current_balance: number
  opening_date?: string
  is_active: boolean
  notes?: string
  created_at: string
  updated_at: string
}

export interface AccountCreate {
  account_name: string
  account_number?: string
  bank_name?: string
  account_type?: string
  currency?: string
  initial_balance: number
  opening_date?: string
  notes?: string
}

export interface AccountUpdate {
  account_name?: string
  account_number?: string
  notes?: string
  is_active?: boolean
}

export interface AccountSummary {
  account: Account
  total_income: number
  total_expense: number
  net_change: number
  transaction_count: number
}
```

#### `types/transaction.ts`
```typescript
export type TransactionType = 'DEBIT' | 'CREDIT'
export type TransactionSource = 'MANUAL' | 'PDF_IMPORT' | 'API'

export interface Transaction {
  id: string
  account_id: string
  transaction_date: string
  description: string
  original_description?: string
  transaction_type: TransactionType
  amount: number
  balance_after?: number
  category_id?: string
  category?: Category
  merchant_id?: string
  merchant?: Merchant
  payment_method?: string
  reference_number?: string
  branch_code?: string
  notes?: string
  is_recurring: boolean
  recurring_id?: string
  source: TransactionSource
  tags?: Tag[]
  created_at: string
  updated_at: string
  created_by: string
}

export interface TransactionCreate {
  account_id: string
  transaction_date: string
  description: string
  transaction_type: TransactionType
  amount: number
  category_id?: string
  merchant_id?: string
  payment_method?: string
  reference_number?: string
  notes?: string
  tags?: string[]
}

export interface TransactionUpdate {
  description?: string
  transaction_date?: string
  amount?: number
  transaction_type?: TransactionType
  category_id?: string
  merchant_id?: string
  payment_method?: string
  notes?: string
}

export interface TransactionFilters {
  account_id?: string
  category_id?: string
  merchant_id?: string
  transaction_type?: TransactionType
  start_date?: string
  end_date?: string
  min_amount?: number
  max_amount?: number
  search?: string
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface TransactionListResponse {
  items: Transaction[]
  total: number
  page: number
  page_size: number
  total_pages: number
}
```

#### `types/category.ts`
```typescript
export type CategoryType = 'INCOME' | 'EXPENSE' | 'TRANSFER'

export interface Category {
  id: string
  user_id?: string
  name: string
  parent_id?: string
  parent?: Category
  children?: Category[]
  type: CategoryType
  icon?: string
  color?: string
  is_system: boolean
  order_index: number
  created_at: string
  updated_at: string
}

export interface CategoryCreate {
  name: string
  parent_id?: string
  type: CategoryType
  icon?: string
  color?: string
}

export interface CategoryUpdate {
  name?: string
  parent_id?: string
  icon?: string
  color?: string
  order_index?: number
}

export interface CategoryTree extends Category {
  children: CategoryTree[]
}
```

#### `types/budget.ts`
```typescript
export type PeriodType = 'WEEKLY' | 'MONTHLY' | 'QUARTERLY' | 'YEARLY'

export interface Budget {
  id: string
  user_id: string
  account_id?: string
  category_id: string
  category?: Category
  name: string
  amount: number
  period_type: PeriodType
  start_date: string
  end_date: string
  alert_threshold: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface BudgetCreate {
  name: string
  category_id: string
  account_id?: string
  amount: number
  period_type: PeriodType
  start_date: string
  end_date: string
  alert_threshold?: number
}

export interface BudgetUpdate {
  name?: string
  amount?: number
  alert_threshold?: number
  is_active?: boolean
}

export interface BudgetProgress {
  budget: Budget
  spent: number
  remaining: number
  percentage: number
  status: 'on_track' | 'at_risk' | 'exceeded'
  days_remaining: number
}
```

#### `types/api.ts`
```typescript
export interface ApiError {
  detail: string
  status_code?: number
}

export interface PaginationParams {
  page: number
  page_size: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}
```

---

## API Integration

### Composables for API Calls

#### `composables/useApi.ts`
```typescript
import type { ApiError } from '~/types/api'

export const useApi = () => {
  const config = useRuntimeConfig()
  const auth = useAuthStore()
  const toast = useNotification()
  
  const handleError = (error: any) => {
    console.error('API Error:', error)
    
    if (error.response) {
      const status = error.response.status
      const message = error.response._data?.detail || 'An error occurred'
      
      if (status === 401) {
        // Token expired or invalid
        auth.logout()
        navigateTo('/login')
        toast.error('Session expired. Please login again.')
      } else if (status === 403) {
        toast.error('You do not have permission to perform this action')
      } else if (status === 404) {
        toast.error('Resource not found')
      } else if (status >= 500) {
        toast.error('Server error. Please try again later.')
      } else {
        toast.error(message)
      }
    } else if (error.request) {
      toast.error('Network error. Please check your connection.')
    } else {
      toast.error('An unexpected error occurred')
    }
  }
  
  const apiCall = async <T>(
    endpoint: string,
    options: RequestInit & { params?: Record<string, any> } = {}
  ): Promise<T> => {
    const token = auth.accessToken
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    try {
      const response = await $fetch<T>(
        `${config.public.apiBaseUrl}${endpoint}`,
        {
          ...options,
          headers,
          // Query params
          ...(options.params && { params: options.params }),
        }
      )
      
      return response
    } catch (error: any) {
      handleError(error)
      throw error
    }
  }
  
  return { apiCall }
}
```

#### `composables/useTransactions.ts`
```typescript
import type {
  Transaction,
  TransactionCreate,
  TransactionUpdate,
  TransactionFilters,
  TransactionListResponse,
} from '~/types/transaction'

export const useTransactions = () => {
  const { apiCall } = useApi()
  
  const getTransactions = async (
    filters: TransactionFilters = {}
  ): Promise<TransactionListResponse> => {
    return await apiCall<TransactionListResponse>('/transactions', {
      method: 'GET',
      params: filters,
    })
  }
  
  const getTransaction = async (id: string): Promise<Transaction> => {
    return await apiCall<Transaction>(`/transactions/${id}`, {
      method: 'GET',
    })
  }
  
  const createTransaction = async (
    data: TransactionCreate
  ): Promise<Transaction> => {
    return await apiCall<Transaction>('/transactions', {
      method: 'POST',
      body: data,
    })
  }
  
  const updateTransaction = async (
    id: string,
    data: TransactionUpdate
  ): Promise<Transaction> => {
    return await apiCall<Transaction>(`/transactions/${id}`, {
      method: 'PUT',
      body: data,
    })
  }
  
  const deleteTransaction = async (id: string): Promise<void> => {
    await apiCall<void>(`/transactions/${id}`, {
      method: 'DELETE',
    })
  }
  
  const updateTransactionCategory = async (
    id: string,
    categoryId: string
  ): Promise<Transaction> => {
    return await apiCall<Transaction>(`/transactions/${id}/category`, {
      method: 'PATCH',
      body: { category_id: categoryId },
    })
  }
  
  return {
    getTransactions,
    getTransaction,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    updateTransactionCategory,
  }
}
```

#### `composables/useAccounts.ts`
```typescript
import type {
  Account,
  AccountCreate,
  AccountUpdate,
  AccountSummary,
} from '~/types/account'

export const useAccounts = () => {
  const { apiCall } = useApi()
  
  const getAccounts = async (): Promise<Account[]> => {
    return await apiCall<Account[]>('/accounts', {
      method: 'GET',
    })
  }
  
  const getAccount = async (id: string): Promise<Account> => {
    return await apiCall<Account>(`/accounts/${id}`, {
      method: 'GET',
    })
  }
  
  const createAccount = async (data: AccountCreate): Promise<Account> => {
    return await apiCall<Account>('/accounts', {
      method: 'POST',
      body: data,
    })
  }
  
  const updateAccount = async (
    id: string,
    data: AccountUpdate
  ): Promise<Account> => {
    return await apiCall<Account>(`/accounts/${id}`, {
      method: 'PUT',
      body: data,
    })
  }
  
  const deleteAccount = async (id: string): Promise<void> => {
    await apiCall<void>(`/accounts/${id}`, {
      method: 'DELETE',
    })
  }
  
  const getAccountSummary = async (
    id: string,
    startDate?: string,
    endDate?: string
  ): Promise<AccountSummary> => {
    return await apiCall<AccountSummary>(`/accounts/${id}/summary`, {
      method: 'GET',
      params: { start_date: startDate, end_date: endDate },
    })
  }
  
  return {
    getAccounts,
    getAccount,
    createAccount,
    updateAccount,
    deleteAccount,
    getAccountSummary,
  }
}
```

---

## State Management

### Pinia Stores

#### `stores/auth.ts`
```typescript
import { defineStore } from 'pinia'
import type { User, LoginRequest, RegisterRequest, AuthResponse } from '~/types/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    accessToken: null as string | null,
    refreshToken: null as string | null,
    isLoading: false,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    currentUser: (state) => state.user,
  },
  
  actions: {
    async login(credentials: LoginRequest) {
      this.isLoading = true
      try {
        const response = await $fetch<AuthResponse>(
          `${useRuntimeConfig().public.apiBaseUrl}/auth/login`,
          {
            method: 'POST',
            body: credentials,
          }
        )
        
        this.accessToken = response.access_token
        this.refreshToken = response.refresh_token
        this.user = response.user
        
        // Store in localStorage
        if (process.client) {
          localStorage.setItem('accessToken', this.accessToken)
          localStorage.setItem('refreshToken', this.refreshToken)
        }
        
        return response
      } catch (error) {
        console.error('Login error:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async register(userData: RegisterRequest) {
      this.isLoading = true
      try {
        const response = await $fetch<AuthResponse>(
          `${useRuntimeConfig().public.apiBaseUrl}/auth/register`,
          {
            method: 'POST',
            body: userData,
          }
        )
        
        this.accessToken = response.access_token
        this.refreshToken = response.refresh_token
        this.user = response.user
        
        if (process.client) {
          localStorage.setItem('accessToken', this.accessToken)
          localStorage.setItem('refreshToken', this.refreshToken)
        }
        
        return response
      } catch (error) {
        console.error('Register error:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async logout() {
      try {
        if (this.accessToken) {
          await $fetch(
            `${useRuntimeConfig().public.apiBaseUrl}/auth/logout`,
            {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${this.accessToken}`,
              },
            }
          )
        }
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.user = null
        this.accessToken = null
        this.refreshToken = null
        
        if (process.client) {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
        }
        
        await navigateTo('/login')
      }
    },
    
    async fetchCurrentUser() {
      if (!this.accessToken) return
      
      try {
        const user = await $fetch<User>(
          `${useRuntimeConfig().public.apiBaseUrl}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        )
        this.user = user
      } catch (error) {
        console.error('Fetch user error:', error)
        this.logout()
      }
    },
    
    async refreshAccessToken() {
      if (!this.refreshToken) return
      
      try {
        const response = await $fetch<{ access_token: string }>(
          `${useRuntimeConfig().public.apiBaseUrl}/auth/refresh`,
          {
            method: 'POST',
            body: { refresh_token: this.refreshToken },
          }
        )
        
        this.accessToken = response.access_token
        
        if (process.client) {
          localStorage.setItem('accessToken', this.accessToken)
        }
      } catch (error) {
        console.error('Token refresh error:', error)
        this.logout()
      }
    },
    
    initializeAuth() {
      if (process.client) {
        const accessToken = localStorage.getItem('accessToken')
        const refreshToken = localStorage.getItem('refreshToken')
        
        if (accessToken && refreshToken) {
          this.accessToken = accessToken
          this.refreshToken = refreshToken
          this.fetchCurrentUser()
        }
      }
    },
  },
})
```

#### `stores/transactions.ts`
```typescript
import { defineStore } from 'pinia'
import type { Transaction, TransactionFilters } from '~/types/transaction'

export const useTransactionStore = defineStore('transactions', {
  state: () => ({
    transactions: [] as Transaction[],
    currentTransaction: null as Transaction | null,
    filters: {} as TransactionFilters,
    total: 0,
    page: 1,
    pageSize: 20,
    isLoading: false,
  }),
  
  getters: {
    paginatedTransactions: (state) => state.transactions,
    totalPages: (state) => Math.ceil(state.total / state.pageSize),
  },
  
  actions: {
    async fetchTransactions(filters?: TransactionFilters) {
      this.isLoading = true
      const { getTransactions } = useTransactions()
      
      try {
        const response = await getTransactions({
          ...this.filters,
          ...filters,
          page: this.page,
          page_size: this.pageSize,
        })
        
        this.transactions = response.items
        this.total = response.total
      } catch (error) {
        console.error('Error fetching transactions:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchTransaction(id: string) {
      this.isLoading = true
      const { getTransaction } = useTransactions()
      
      try {
        this.currentTransaction = await getTransaction(id)
      } catch (error) {
        console.error('Error fetching transaction:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    setFilters(filters: TransactionFilters) {
      this.filters = filters
      this.page = 1
      this.fetchTransactions()
    },
    
    setPage(page: number) {
      this.page = page
      this.fetchTransactions()
    },
    
    clearFilters() {
      this.filters = {}
      this.page = 1
      this.fetchTransactions()
    },
  },
})
```

---

## Components

### Common Components

#### `components/common/AppButton.vue`
```vue
<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
  type: 'button',
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => {
  const base = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
  }
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }
  
  const disabled = props.disabled || props.loading ? 'opacity-50 cursor-not-allowed' : ''
  
  return [base, variants[props.variant], sizes[props.size], disabled].join(' ')
})

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="mr-2">
      <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
    </span>
    <slot />
  </button>
</template>
```

#### `components/common/AppInput.vue`
```vue
<script setup lang="ts">
interface Props {
  modelValue: string | number
  type?: 'text' | 'email' | 'password' | 'number' | 'tel'
  label?: string
  placeholder?: string
  error?: string
  disabled?: boolean
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
}>()

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const inputClasses = computed(() => {
  const base = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
  const error = props.error ? 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:ring-red-500' : ''
  const disabled = props.disabled ? 'bg-gray-100 cursor-not-allowed' : ''
  
  return [base, error, disabled].join(' ')
})
</script>

<template>
  <div>
    <label v-if="label" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      v-model="inputValue"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :class="inputClasses"
    />
    <p v-if="error" class="mt-1 text-sm text-red-600">
      {{ error }}
    </p>
  </div>
</template>
```

### Transaction Components

#### `components/transactions/TransactionForm.vue`
```vue
<script setup lang="ts">
import type { TransactionCreate, TransactionType } from '~/types/transaction'
import type { Account } from '~/types/account'
import type { Category } from '~/types/category'

interface Props {
  transaction?: Transaction
  mode?: 'create' | 'edit'
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'create',
})

const emit = defineEmits<{
  submit: [data: TransactionCreate]
  cancel: []
}>()

const { getAccounts } = useAccounts()
const { getCategories } = useCategories()

const accounts = ref<Account[]>([])
const categories = ref<Category[]>([])
const isLoading = ref(false)

const form = reactive<TransactionCreate>({
  account_id: props.transaction?.account_id || '',
  transaction_date: props.transaction?.transaction_date || new Date().toISOString(),
  description: props.transaction?.description || '',
  transaction_type: props.transaction?.transaction_type || 'DEBIT',
  amount: props.transaction?.amount || 0,
  category_id: props.transaction?.category_id,
  payment_method: props.transaction?.payment_method,
  notes: props.transaction?.notes,
})

const errors = reactive<Partial<Record<keyof TransactionCreate, string>>>({})

onMounted(async () => {
  accounts.value = await getAccounts()
  categories.value = await getCategories({ type: 'EXPENSE' })
})

const validate = (): boolean => {
  Object.keys(errors).forEach(key => delete errors[key as keyof typeof errors])
  
  if (!form.account_id) {
    errors.account_id = 'Account is required'
  }
  if (!form.description) {
    errors.description = 'Description is required'
  }
  if (!form.amount || form.amount <= 0) {
    errors.amount = 'Amount must be greater than 0'
  }
  if (!form.transaction_date) {
    errors.transaction_date = 'Date is required'
  }
  
  return Object.keys(errors).length === 0
}

const handleSubmit = () => {
  if (validate()) {
    emit('submit', form)
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <AppSelect
      v-model="form.account_id"
      label="Account"
      :options="accounts"
      option-label="account_name"
      option-value="id"
      :error="errors.account_id"
      required
    />
    
    <AppInput
      v-model="form.description"
      label="Description"
      placeholder="e.g., Coffee at Starbucks"
      :error="errors.description"
      required
    />
    
    <div class="grid grid-cols-2 gap-4">
      <AppSelect
        v-model="form.transaction_type"
        label="Type"
        :options="[
          { label: 'Expense', value: 'DEBIT' },
          { label: 'Income', value: 'CREDIT' }
        ]"
        option-label="label"
        option-value="value"
        required
      />
      
      <AppInput
        v-model.number="form.amount"
        type="number"
        label="Amount"
        placeholder="0"
        :error="errors.amount"
        required
      />
    </div>
    
    <AppDatePicker
      v-model="form.transaction_date"
      label="Date"
      :error="errors.transaction_date"
      required
    />
    
    <AppSelect
      v-model="form.category_id"
      label="Category"
      :options="categories"
      option-label="name"
      option-value="id"
      placeholder="Select category"
    />
    
    <AppInput
      v-model="form.payment_method"
      label="Payment Method"
      placeholder="e.g., QR, E-Banking, Cash"
    />
    
    <AppTextarea
      v-model="form.notes"
      label="Notes"
      placeholder="Additional notes..."
      rows="3"
    />
    
    <div class="flex justify-end gap-3">
      <AppButton variant="secondary" @click="emit('cancel')">
        Cancel
      </AppButton>
      <AppButton type="submit" :loading="isLoading">
        {{ mode === 'create' ? 'Create' : 'Update' }} Transaction
      </AppButton>
    </div>
  </form>
</template>
```

---

## Utilities

### Currency Formatting

#### `utils/currency.ts`
```typescript
/**
 * Format number to Indonesian Rupiah (IDR)
 * Example: 1234567.89 → Rp 1.234.567,89
 */
export const formatIDR = (amount: number): string => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount)
}

/**
 * Format number to Indonesian format without currency symbol
 * Example: 1234567.89 → 1.234.567,89
 */
export const formatNumber = (amount: number): string => {
  return new Intl.NumberFormat('id-ID', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount)
}

/**
 * Parse Indonesian formatted string to number
 * Example: "1.234.567,89" → 1234567.89
 */
export const parseIDR = (formatted: string): number => {
  // Remove currency symbol and spaces
  let cleaned = formatted.replace(/[^\d.,-]/g, '')
  // Replace dots (thousand separators) with nothing
  cleaned = cleaned.replace(/\./g, '')
  // Replace comma (decimal separator) with dot
  cleaned = cleaned.replace(',', '.')
  return parseFloat(cleaned) || 0
}

/**
 * Validate IDR amount string
 */
export const isValidIDRAmount = (amount: string): boolean => {
  // Allow digits, dots, and comma
  const pattern = /^\d{1,3}(\.\d{3})*(,\d{1,2})?$/
  return pattern.test(amount)
}
```

### Date Utilities

#### `utils/date.ts`
```typescript
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/id'

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(relativeTime)
dayjs.locale('id')

/**
 * Format date to Indonesian format
 * Example: 2025-01-15T10:30:00Z → 15/01/2025
 */
export const formatDate = (date: string | Date, format: string = 'DD/MM/YYYY'): string => {
  return dayjs(date).tz('Asia/Jakarta').format(format)
}

/**
 * Format date with time
 * Example: 2025-01-15T10:30:00Z → 15/01/2025 17:30
 */
export const formatDateTime = (date: string | Date): string => {
  return dayjs(date).tz('Asia/Jakarta').format('DD/MM/YYYY HH:mm')
}

/**
 * Format relative time
 * Example: "2 days ago", "in 3 hours"
 */
export const formatRelativeTime = (date: string | Date): string => {
  return dayjs(date).tz('Asia/Jakarta').fromNow()
}

/**
 * Convert to ISO string in UTC
 */
export const toISOString = (date: string | Date): string => {
  return dayjs(date).utc().toISOString()
}

/**
 * Get start of month
 */
export const startOfMonth = (date?: string | Date): string => {
  return dayjs(date).startOf('month').toISOString()
}

/**
 * Get end of month
 */
export const endOfMonth = (date?: string | Date): string => {
  return dayjs(date).endOf('month').toISOString()
}

/**
 * Get month name
 */
export const getMonthName = (monthIndex: number): string => {
  const months = [
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
  ]
  return months[monthIndex]
}
```

---

## Development Guidelines

### Code Standards

```typescript
// File naming
- Components: PascalCase (TransactionList.vue)
- Composables: camelCase with 'use' prefix (useTransactions.ts)
- Utilities: camelCase (currency.ts)
- Types: camelCase (transaction.ts)

// Component structure
<script setup lang="ts">
// 1. Imports
import type { Transaction } from '~/types/transaction'

// 2. Props & Emits
interface Props {
  transaction: Transaction
}

const props = defineProps<Props>()
const emit = defineEmits<{
  update: [transaction: Transaction]
}>()

// 3. Composables
const { formatIDR } = useCurrency()

// 4. Reactive state
const isEditing = ref(false)

// 5. Computed
const formattedAmount = computed(() => formatIDR(props.transaction.amount))

// 6. Methods
const handleEdit = () => {
  isEditing.value = true
}

// 7. Lifecycle hooks
onMounted(() => {
  // ...
})
</script>

<template>
  <!-- Template -->
</template>

<style scoped>
/* Scoped styles */
</style>
```

### Naming Conventions

```typescript
// Variables & Functions
const userName = ref('')
const fetchUserData = async () => {}

// Constants
const MAX_FILE_SIZE = 5 * 1024 * 1024
const API_TIMEOUT = 30000

// Types & Interfaces
interface UserProfile {}
type TransactionType = 'DEBIT' | 'CREDIT'

// Components (in template)
<TransactionList /> <!-- PascalCase -->
<app-button /> <!-- kebab-case also acceptable -->
```

---

## Testing

### Component Testing

```typescript
// tests/components/TransactionForm.spec.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import TransactionForm from '~/components/transactions/TransactionForm.vue'

describe('TransactionForm', () => {
  it('validates required fields', async () => {
    const wrapper = mount(TransactionForm)
    
    await wrapper.find('form').trigger('submit')
    
    expect(wrapper.find('.error').text()).toContain('required')
  })
  
  it('emits submit event with form data', async () => {
    const wrapper = mount(TransactionForm)
    
    await wrapper.find('input[name="amount"]').setValue('100000')
    await wrapper.find('input[name="description"]').setValue('Test')
    await wrapper.find('form').trigger('submit')
    
    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})
```

---

## Deployment

### Environment Variables

```env
# .env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NUXT_PUBLIC_APP_NAME=Money Tracker
NUXT_PUBLIC_ENVIRONMENT=development
```

### Build & Run

```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Generate static site
npm run generate
```

### nuxt.config.ts

```typescript
export default defineNuxtConfig({
  modules: ['@pinia/nuxt'],
  
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
      appName: process.env.NUXT_PUBLIC_APP_NAME || 'Money Tracker',
      environment: process.env.NUXT_PUBLIC_ENVIRONMENT || 'development',
    }
  },
  
  css: ['~/assets/css/main.css'],
  
  typescript: {
    strict: true,
    typeCheck: true,
  },
  
  devtools: { enabled: true },
})
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-25
