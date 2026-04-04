<script setup lang="ts">
defineProps<{
  columns: string[]
  rows: Record<string, unknown>[]
  totalRows: number
  page: number
  pageSize: number
  isLoading: boolean
}>()

const emit = defineEmits<{
  pageChange: [page: number]
}>()

function totalPages(totalRows: number, pageSize: number) {
  return Math.ceil(totalRows / pageSize)
}
</script>

<template>
  <div class="flex flex-col min-h-0 flex-1">
    <div class="overflow-auto border rounded-lg max-h-[60vh]">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-50 sticky top-0">
          <tr>
            <th
              v-for="col in columns"
              :key="col"
              class="px-4 py-2 text-left font-medium text-gray-600 border-b whitespace-nowrap"
            >
              {{ col }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, idx) in rows"
            :key="idx"
            class="hover:bg-gray-50"
          >
            <td
              v-for="col in columns"
              :key="col"
              class="px-4 py-2 border-b text-gray-700 whitespace-nowrap"
            >
              {{ row[col] ?? '' }}
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="isLoading" class="flex items-center justify-center py-8 text-gray-400">
        Loading...
      </div>

      <div v-if="!isLoading && rows.length === 0" class="flex items-center justify-center py-8 text-gray-400">
        No data
      </div>
    </div>

    <div class="flex items-center justify-between mt-3 text-sm text-gray-600">
      <span>{{ totalRows }} rows total</span>
      <div class="flex items-center gap-2">
        <button
          :disabled="page <= 1"
          class="px-3 py-1 border rounded disabled:opacity-40"
          @click="emit('pageChange', page - 1)"
        >
          Prev
        </button>
        <span>Page {{ page }} of {{ totalPages(totalRows, pageSize) }}</span>
        <button
          :disabled="page >= totalPages(totalRows, pageSize)"
          class="px-3 py-1 border rounded disabled:opacity-40"
          @click="emit('pageChange', page + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
