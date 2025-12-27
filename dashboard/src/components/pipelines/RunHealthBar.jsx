import React from 'react';

const RunHealthBar = () => {
    return (
        <div className="flex items-center space-x-2 w-full max-w-xs">
            <div className="flex-1 h-2 bg-background-light rounded-full overflow-hidden flex">
                <div className="h-full bg-success-light w-[85%]"></div>
                <div className="h-full bg-danger-light w-[15%]"></div>
            </div>
            <span className="text-xs text-muted-light font-medium">85% Success Rate</span>
        </div>
    );
};

export default RunHealthBar;
