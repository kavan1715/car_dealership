import React from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';

export const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const isFirstPage = currentPage === 1;
  const isLastPage = currentPage === totalPages || totalPages === 0;

  return (
    <div className="flex items-center justify-between border-t border-slate-800/80 px-4 py-4 sm:px-6">
      <div className="flex flex-1 justify-between sm:hidden">
        <button
          onClick={() => !isFirstPage && onPageChange(currentPage - 1)}
          disabled={isFirstPage}
          className={`relative inline-flex items-center rounded-lg px-4 py-2 text-sm font-medium border ${
            isFirstPage
              ? 'border-slate-800 text-slate-600 bg-[#0d121f] cursor-not-allowed'
              : 'border-slate-700 text-slate-300 bg-[#151c2c] hover:bg-[#1a2336] transition-colors'
          }`}
        >
          Previous
        </button>
        <span className="text-slate-400 text-sm flex items-center">
          Page {currentPage} of {totalPages || 1}
        </span>
        <button
          onClick={() => !isLastPage && onPageChange(currentPage + 1)}
          disabled={isLastPage}
          className={`relative ml-3 inline-flex items-center rounded-lg px-4 py-2 text-sm font-medium border ${
            isLastPage
              ? 'border-slate-800 text-slate-600 bg-[#0d121f] cursor-not-allowed'
              : 'border-slate-700 text-slate-300 bg-[#151c2c] hover:bg-[#1a2336] transition-colors'
          }`}
        >
          Next
        </button>
      </div>

      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-slate-400">
            Showing <span className="font-semibold text-slate-200">Page {currentPage}</span> of{' '}
            <span className="font-semibold text-slate-200">{totalPages || 1}</span> pages
          </p>
        </div>
        <div>
          <nav className="isolate inline-flex -space-x-px rounded-xl shadow-sm gap-2" aria-label="Pagination">
            <button
              onClick={() => !isFirstPage && onPageChange(currentPage - 1)}
              disabled={isFirstPage}
              className={`relative inline-flex items-center rounded-xl p-2.5 text-sm font-medium border ${
                isFirstPage
                  ? 'border-slate-800 text-slate-600 bg-[#0d121f] cursor-not-allowed'
                  : 'border-slate-700 text-slate-300 bg-[#151c2c] hover:bg-[#1a2336] transition-colors'
              }`}
            >
              <span className="sr-only">Previous</span>
              <ArrowLeft className="h-4 sm:h-5 w-4 sm:w-5" aria-hidden="true" />
            </button>
            <span className="inline-flex items-center px-4 text-sm font-medium text-slate-300">
              Page {currentPage} of {totalPages || 1}
            </span>
            <button
              onClick={() => !isLastPage && onPageChange(currentPage + 1)}
              disabled={isLastPage}
              className={`relative inline-flex items-center rounded-xl p-2.5 text-sm font-medium border ${
                isLastPage
                  ? 'border-slate-800 text-slate-600 bg-[#0d121f] cursor-not-allowed'
                  : 'border-slate-700 text-slate-300 bg-[#151c2c] hover:bg-[#1a2336] transition-colors'
              }`}
            >
              <span className="sr-only">Next</span>
              <ArrowRight className="h-4 sm:h-5 w-4 sm:w-5" aria-hidden="true" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  );
};
