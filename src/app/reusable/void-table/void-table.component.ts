import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DataTablesModule } from 'angular-datatables';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-void-table',
  standalone: true,
  imports: [CommonModule, FormsModule, DataTablesModule],
  templateUrl: './void-table.component.html',
  styleUrl: './void-table.component.css'
})
export class VoidTableComponent implements OnChanges {

  [x: string]: any;
  paging(arg0: any, arg1: any) {
    throw new Error('Method not implemented.');
  }

  currentPage: number = 1;
  pageSize: number = 5;
  totalPages: number = 0;

  @Input() tableData: any[] = [];
  @Input() columnArray: any[] = [];

  @Output() onEdit = new EventEmitter<any>();
  @Output() onDelete = new EventEmitter<any>();

  @Input() showActionButton: Boolean = false;

  filteredData: any[] = [];
  searchBox: string = '';
  dtoptions: DataTables.Settings = {};
  dttrigger: Subject<any>= new Subject<any>();

  constructor() {
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.dtoptions = { pagingType: 'full_numbers' };
    this.filteredData = this.tableData;
    this.calculateTotalPages();
  }


  calculateTotalPages() {
    this.totalPages = Math.ceil(this.filteredData.length / this.pageSize);
  }

  onSearchChange(searchVal: string): void {
    this.filteredData = this.tableData.filter((searchData: any) => {
      const values = Object.values(searchData);
      let flag = false;
      values.forEach((val: any) => {
        if (val.toString().toLowerCase().indexOf(searchVal) > -1) {
          flag = true;
          return;
        }
      });
      if (flag) {
        return searchData;
      }
    });

    this.calculateTotalPages();
  }
  editRecord(item: any) {
    debugger
    this.onEdit.emit(item);
  }

  deleteRecord(item: any) {
    debugger
    this.onDelete.emit(item);
  }

  goToPage(pageNumber: number) {
    if (pageNumber >= 1 && pageNumber <= this.totalPages) {
      this.currentPage = pageNumber;
      this.filteredData = this.tableData.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);
    }
  }
}
