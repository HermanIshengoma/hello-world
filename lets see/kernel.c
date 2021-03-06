/* kernel.c
 * COS 318, Fall 2019: Project 2 Non-Preemptive Kernel
 * Entry point that runs when the bootloader transfers control to the kernel
 */

#include "common.h"
#include "kernel.h"
#include "scheduler.h"
#include "th.h"
#include "util.h"

#include "tasks.c"

void zero_entry();
pcb_t *current_running;
uint32_t to_store;
uint32_t to_store2;

// Kernel entry point must be the first function in the file
void _start(void) {
    // Set up the single entry point for system calls
    *ENTRY_POINT = &kernel_entry;
    
    clear_screen(0, 0, 80, 25);

    // Initialize the pcbs and the ready queue
    // allocate space for the PCBs statically with pcb_t pcbs[NUM_TASKS]
    //print_str(4, 0, "I am here");
    static pcb_t pcbs[NUM_TASKS];
    // static pcb_t* red_arr[NUM_TASKS];
    // queue_init(&ready, red_arr[0], NUM_TASKS);
    
    // Make sure to loop on NUM_TASKS when setting up PCBs as the number of tasks may be different during testing
    int i = 0;
    while (i < NUM_TASKS){
        pcbs[i].pid = i;
        print_int(3, 0, i);

        pcbs[i].stack_start = STACK_MIN + (i * STACK_SIZE);

        // initialize stack pointer at start of stack?
        pcbs[i].stack_pointer = pcbs[i].stack_start;

        print_hex(4, 0, pcbs[i].stack_pointer);
        pcbs[i].ran = 0;
        pcbs[i].cpu_time_used = get_timer();

        pcbs[i].task = task[i];
        pcbs[i].entry = (*task[i]).entry_point;
        
        // add to the ready queue as well
        // enqueue(&ready, &pcbs[i]);
        
        // zero all registers and set stack pointer to stack_start
        current_running = &pcbs[i];
        zero_entry();
        print_hex(5, 0, pcbs[i].stack_pointer);
        i++;
    }
        

    // initialize ready queue
    current_running = &pcbs[0];
    
    // Schedule the first task
    scheduler_count = 0;
    //zero_entry();
    scheduler_entry();
    
    // we should never reach here
    ASSERT(0);
}
