import { searchObservations, getObservation } from '../src/mcp-tools';

describe('MCP Tool Wrappers', () => {
  test('should return empty array for search (mock)', async () => {
    const results = await searchObservations('test', 10, 'project');

    expect(results).toEqual([]);
  });

  test('should return null for getObservation (mock)', async () => {
    const result = await getObservation(1, 'project');

    expect(result).toBeNull();
  });
});
