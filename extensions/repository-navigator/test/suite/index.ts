/**
 * Test Suite Index - Loads all integration and E2E tests
 * Agent-6 (VSCode Forking Lead) - Team Beta Week 4 Phase 1 Day 3
 */

import * as path from 'path';
import Mocha from 'mocha';
import { glob } from 'glob';

export function run(): Promise<void> {
    // Create the mocha test
    const mocha = new Mocha({
        ui: 'tdd',
        color: true,
        timeout: 10000 // 10 second timeout for integration tests
    });

    const testsRoot = path.resolve(__dirname);

    return new Promise((resolve, reject) => {
        // Find all integration and e2e test files
        glob('**/**.test.js', { cwd: testsRoot })
            .then((files) => {
                // Add files to the test suite
                files.forEach(f => mocha.addFile(path.resolve(testsRoot, f)));

                try {
                    // Run the mocha test
                    mocha.run(failures => {
                        if (failures > 0) {
                            reject(new Error(`${failures} tests failed.`));
                        } else {
                            resolve();
                        }
                    });
                } catch (err) {
                    console.error(err);
                    reject(err);
                }
            })
            .catch((err) => {
                reject(err);
            });
    });
}

