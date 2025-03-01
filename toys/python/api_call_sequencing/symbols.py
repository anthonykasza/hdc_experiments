from utils import hdv

function_names = [
  "alloc_page",
  "bitmap_copy",
  "block_io",
  "cpu_online",
  "dma_alloc_coherent",
  "dma_free_coherent",
  "do_fork",
  "do_sys_open",
  "file_operations",
  "free_page",
  "get_cpu_var",
  "get_user_pages",
  "hrtimer_init",
  "irq_set_handler",
  "kmalloc",
  "kmem_cache_create",
  "kmem_cache_destroy",
  "mempool_alloc",
  "mempool_free",
  "mprotect",
  "printk",
  "put_user",
  "read_lock",
  "request_irq",
  "schedule"
]

function_symbols = [hdv() for name in function_names]
