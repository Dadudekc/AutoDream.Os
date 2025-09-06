/**
 * Vector Database Search - V2 Compliant Module
 * ===========================================
 *
 * Search functionality for vector database operations.
 * Handles search queries, filtering, and result processing.
 *
 * V2 Compliance: < 300 lines, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class VectorDatabaseSearch {
    constructor(core) {
        this.core = core;
        this.searchHistory = [];
        this.searchCache = new Map();
        this.logger = console;
    }

    /**
     * Perform search with advanced filtering
     */
    async search(query, options = {}) {
        try {
            const searchId = `search_${Date.now()}`;
            const startTime = Date.now();

            // Check cache first
            const cacheKey = this.getCacheKey(query, options);
            if (this.searchCache.has(cacheKey)) {
                this.logger.log('🔍 Search result from cache');
                return this.searchCache.get(cacheKey);
            }

            // Perform search
            const results = await this.core.searchDocuments(query, options);

            // Process results
            const processedResults = this.processSearchResults(results, options);

            // Update search history
            this.updateSearchHistory(query, processedResults);

            // Cache results
            this.searchCache.set(cacheKey, processedResults);

            // Log performance
            const searchTime = Date.now() - startTime;
            this.logger.log(`🔍 Search completed in ${searchTime}ms: ${processedResults.length} results`);

            return processedResults;
        } catch (error) {
            this.logger.error('❌ Search failed:', error);
            throw error;
        }
    }

    /**
     * Process search results
     */
    processSearchResults(results, options) {
        return results.map(result => ({
            ...result,
            relevanceScore: this.calculateRelevanceScore(result, options),
            highlightedContent: this.highlightSearchTerms(result.content, options.query),
            categories: this.categorizeResult(result),
            tags: this.extractTags(result)
        }));
    }

    /**
     * Calculate relevance score
     */
    calculateRelevanceScore(result, options) {
        let score = result.score || 0;

        // Boost score for exact matches
        if (result.title && result.title.toLowerCase().includes(options.query?.toLowerCase())) {
            score += 0.2;
        }

        // Boost score for recent documents
        if (result.metadata?.created) {
            const age = Date.now() - result.metadata.created;
            const ageInDays = age / (1000 * 60 * 60 * 24);
            if (ageInDays < 7) score += 0.1;
        }

        return Math.min(score, 1.0);
    }

    /**
     * Highlight search terms in content
     */
    highlightSearchTerms(content, query) {
        if (!query || !content) return content;

        const terms = query.toLowerCase().split(' ').filter(term => term.length > 2);
        let highlighted = content;

        terms.forEach(term => {
            const regex = new RegExp(`(${term})`, 'gi');
            highlighted = highlighted.replace(regex, '<mark>$1</mark>');
        });

        return highlighted;
    }

    /**
     * Categorize search result
     */
    categorizeResult(result) {
        const categories = [];

        if (result.metadata?.type) {
            categories.push(result.metadata.type);
        }

        if (result.content?.length > 500) {
            categories.push('long-form');
        } else if (result.content?.length < 100) {
            categories.push('short-form');
        }

        return categories;
    }

    /**
     * Extract tags from result
     */
    extractTags(result) {
        const tags = [];

        // Extract tags from metadata
        if (result.metadata?.tags) {
            tags.push(...result.metadata.tags);
        }

        // Extract potential tags from content
        const content = result.content || '';
        const words = content.toLowerCase().split(/\s+/);
        const commonWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);

        const wordCount = {};
        words.forEach(word => {
            if (word.length > 3 && !commonWords.has(word)) {
                wordCount[word] = (wordCount[word] || 0) + 1;
            }
        });

        // Get top 3 most frequent words as tags
        const topWords = Object.entries(wordCount)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3)
            .map(([word]) => word);

        tags.push(...topWords);

        return [...new Set(tags)]; // Remove duplicates
    }

    /**
     * Update search history
     */
    updateSearchHistory(query, results) {
        const searchEntry = {
            query,
            resultCount: results.length,
            timestamp: Date.now(),
            results: results.slice(0, 5) // Store only first 5 results
        };

        this.searchHistory.unshift(searchEntry);

        // Keep only last 50 searches
        if (this.searchHistory.length > 50) {
            this.searchHistory = this.searchHistory.slice(0, 50);
        }
    }

    /**
     * Get search history
     */
    getSearchHistory(limit = 10) {
        return this.searchHistory.slice(0, limit);
    }

    /**
     * Get popular searches
     */
    getPopularSearches() {
        const queryCount = {};

        this.searchHistory.forEach(entry => {
            queryCount[entry.query] = (queryCount[entry.query] || 0) + 1;
        });

        return Object.entries(queryCount)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10)
            .map(([query, count]) => ({ query, count }));
    }

    /**
     * Get search suggestions
     */
    getSearchSuggestions(partialQuery) {
        if (!partialQuery || partialQuery.length < 2) return [];

        const suggestions = new Set();

        // Get suggestions from search history
        this.searchHistory.forEach(entry => {
            if (entry.query.toLowerCase().startsWith(partialQuery.toLowerCase())) {
                suggestions.add(entry.query);
            }
        });

        // Get suggestions from document titles
        // This would typically come from the core database
        const mockSuggestions = [
            'machine learning',
            'artificial intelligence',
            'data science',
            'web development',
            'vector database'
        ];

        mockSuggestions.forEach(suggestion => {
            if (suggestion.toLowerCase().startsWith(partialQuery.toLowerCase())) {
                suggestions.add(suggestion);
            }
        });

        return Array.from(suggestions).slice(0, 5);
    }

    /**
     * Clear search cache
     */
    clearSearchCache() {
        this.searchCache.clear();
        this.logger.log('🧹 Search cache cleared');
    }

    /**
     * Get cache key for search
     */
    getCacheKey(query, options) {
        return `${query}_${JSON.stringify(options)}`;
    }

    /**
     * Get search statistics
     */
    getSearchStats() {
        return {
            totalSearches: this.searchHistory.length,
            cacheSize: this.searchCache.size,
            averageResults: this.searchHistory.length > 0
                ? this.searchHistory.reduce((sum, entry) => sum + entry.resultCount, 0) / this.searchHistory.length
                : 0
        };
    }

    /**
     * Export search data
     */
    exportSearchData() {
        return {
            history: this.searchHistory,
            stats: this.getSearchStats(),
            popularSearches: this.getPopularSearches()
        };
    }
}
