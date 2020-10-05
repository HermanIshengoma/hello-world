/* kernel.h
 * COS 318, Fall 2019: Project 2 Non-Preemptive Kernel
 * Definitions and types used by kernel code
 */

#ifndef KERNEL_H
#define KERNEL_H

#include "common.h"

// ENTRY_POINT points to a location that holds a pointer to kernel_entry
#define ENTRY_POINT ((void (**)(int)) 0x0f00)

// System call numbers
enum {
    SYSCALL_YIELD,
    SYSCALL_EXIT,
};

// All stacks should be STACK_SIZE bytes large
// The first stack should be placed at location STACK_MIN
// Only memory below STACK_MAX should be used for stacks
enum {
    STACK_MIN = 0x40000,
    STACK_SIZE = 0x1000,
    STACK_MAX = 0x52000,
};

typedef struct pcb {
    uint32_t stack_pointer; // where the stack pointer points for this pcb
    uint32_t ran;
    uint32_t entry;
    uint32_t stack_start;   // where the stack of this pcb begins
    uint32_t pid;           // process id
    uint64_t cpu_time_used; //
    struct task_info *task;
    
} pcb_t;

// The task currently running
extern pcb_t *current_running;

void kernel_entry(int fn);

#endif
