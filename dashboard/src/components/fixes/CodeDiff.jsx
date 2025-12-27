import React from 'react';

const CodeDiff = () => {
    return (
        <div className="font-mono text-sm border border-border-light rounded-lg overflow-hidden">
            <div className="bg-background-light px-4 py-2 border-b border-border-light text-muted-dark text-xs flex justify-between">
                <span>src/auth/login.php</span>
                <span>Lines 24-28</span>
            </div>
            <div className="bg-white p-4 overflow-x-auto">
                <div className="flex">
                    <div className="text-right pr-4 text-muted-light select-none border-r border-border-light mr-4">
                        <div className="text-danger-dark opacity-50">24</div>
                        <div className="text-success-dark opacity-50">25</div>
                    </div>
                    <div className="w-full">
                        <div className="bg-danger-light/10 text-danger-dark w-full block mb-1">
                            - $query = "SELECT * FROM users WHERE username = '" . $username . "'";
                        </div>
                        <div className="bg-success-light/10 text-success-light w-full block">
                            + $stmt = $pdo-&gt;prepare("SELECT * FROM users WHERE username = ?");
                        </div>
                        <div className="bg-success-light/10 text-success-light w-full block">
                            + $stmt-&gt;execute([$username]);
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CodeDiff;
