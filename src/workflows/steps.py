"""
Workflow Step Builders - V2 Compliant
=====================================

Specialized builders for creating workflow steps and patterns.
Provides high-level abstractions for common workflow patterns.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive type hints.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

from typing import Any

from .models import CoordinationStrategy, ResponseType, WorkflowStep


class WorkflowStepBuilder:
    """
    Base builder for workflow steps.

    Provides common functionality for creating workflow steps
    with proper dependency management and configuration.
    """

    def __init__(self):
        self.steps: list[WorkflowStep] = []
        self.step_counter = 0

    def create_step(
        self,
        name: str,
        description: str,
        agent_target: str,
        prompt_template: str,
        expected_response_type: ResponseType,
        timeout_seconds: int = 300,
        dependencies: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> WorkflowStep:
        """Create a basic workflow step."""
        step_id = f"step_{self.step_counter}"
        self.step_counter += 1

        step = WorkflowStep(
            id=step_id,
            name=name,
            description=description,
            agent_target=agent_target,
            prompt_template=prompt_template,
            expected_response_type=expected_response_type,
            timeout_seconds=timeout_seconds,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self.steps.append(step)
        return step

    def get_steps(self) -> list[WorkflowStep]:
        """Get all created steps."""
        return self.steps.copy()


class ConversationLoopBuilder(WorkflowStepBuilder):
    """
    Builder for conversation loop workflows.

    Creates a series of steps for agents to have structured conversations
    with dependency management between rounds.
    """

    def create_conversation_loop(
        self,
        agent_a: str,
        agent_b: str,
        topic: str,
        iterations: int = 3,
        timeout_per_round: int = 300,
    ) -> list[WorkflowStep]:
        """
        Create a conversation loop between two agents.

        Args:
            agent_a: First agent in conversation
            agent_b: Second agent in conversation
            topic: Conversation topic
            iterations: Number of conversation rounds
            timeout_per_round: Timeout for each round

        Returns:
            List of workflow steps for the conversation
        """
        conversation_steps = []

        for i in range(iterations):
            # Agent A prompts Agent B
            step_a_id = f"conversation_{i}_a"
            step_a = self.create_step(
                name=f"Agent {agent_a} prompts {agent_b} - Round {i+1}",
                description=f"Agent {agent_a} asks {agent_b} about {topic}",
                agent_target=agent_a,
                prompt_template=f"Ask Agent {agent_b} about {topic}. Be specific and build on previous responses.",
                expected_response_type=ResponseType.CONVERSATION_PROMPT,
                timeout_seconds=timeout_per_round,
                dependencies=[f"conversation_{i-1}_b"] if i > 0 else [],
                metadata={
                    "conversation_round": i + 1,
                    "topic": topic,
                    "agent_pair": f"{agent_a}-{agent_b}",
                },
            )
            conversation_steps.append(step_a)

            # Agent B responds
            step_b_id = f"conversation_{i}_b"
            step_b = self.create_step(
                name=f"Agent {agent_b} responds to {agent_a} - Round {i+1}",
                description=f"Agent {agent_b} responds to {agent_a} about {topic}",
                agent_target=agent_b,
                prompt_template=f"Respond to Agent {agent_a}'s question about {topic}. Provide detailed, helpful information.",
                expected_response_type=ResponseType.CONVERSATION_RESPONSE,
                timeout_seconds=timeout_per_round,
                dependencies=[step_a_id],
                metadata={
                    "conversation_round": i + 1,
                    "topic": topic,
                    "agent_pair": f"{agent_a}-{agent_b}",
                },
            )
            conversation_steps.append(step_b)

        return conversation_steps


class MultiAgentOrchestrationBuilder(WorkflowStepBuilder):
    """
    Builder for multi-agent orchestration workflows.

    Creates workflows where multiple agents work together
    using different coordination strategies.
    """

    def create_multi_agent_orchestration(
        self,
        task: str,
        agents: list[str],
        strategy: CoordinationStrategy = CoordinationStrategy.PARALLEL,
        timeout_per_agent: int = 300,
    ) -> list[WorkflowStep]:
        """
        Create multi-agent orchestration workflow.

        Args:
            task: Task description for agents to work on
            agents: List of agent IDs to coordinate
            strategy: Coordination strategy (parallel or sequential)
            timeout_per_agent: Timeout for each agent's work

        Returns:
            List of workflow steps for the orchestration
        """
        orchestration_steps = []

        if strategy == CoordinationStrategy.PARALLEL:
            # All agents work in parallel
            for i, agent in enumerate(agents):
                step = self.create_step(
                    name=f"Agent {agent} works on {task}",
                    description=f"Agent {agent} executes task: {task}",
                    agent_target=agent,
                    prompt_template=f"Work on the following task: {task}. Coordinate with other agents as needed.",
                    expected_response_type=ResponseType.TASK_EXECUTION,
                    timeout_seconds=timeout_per_agent,
                    metadata={
                        "task": task,
                        "agent_index": i,
                        "total_agents": len(agents),
                        "strategy": "parallel",
                    },
                )
                orchestration_steps.append(step)

        elif strategy == CoordinationStrategy.SEQUENTIAL:
            # Agents work in sequence, building on each other
            dependencies = []
            for i, agent in enumerate(agents):
                step = self.create_step(
                    name=f"Agent {agent} works on {task} (Step {i+1})",
                    description=f"Agent {agent} executes task: {task} after previous agents",
                    agent_target=agent,
                    prompt_template=f"Continue work on: {task}. Build upon the work of previous agents.",
                    expected_response_type=ResponseType.TASK_EXECUTION,
                    timeout_seconds=timeout_per_agent,
                    dependencies=dependencies.copy(),
                    metadata={
                        "task": task,
                        "agent_index": i,
                        "total_agents": len(agents),
                        "strategy": "sequential",
                    },
                )
                orchestration_steps.append(step)
                dependencies.append(step.id)

        return orchestration_steps


class DecisionTreeBuilder(WorkflowStepBuilder):
    """
    Builder for decision tree workflows.

    Creates workflows with decision points and branching logic
    based on AI responses.
    """

    def create_decision_tree(
        self,
        decision_point: str,
        branches: dict[str, dict[str, Any]],
        decision_agent: str = "Agent-1",
        analysis_timeout: int = 180,
        branch_timeout: int = 300,
    ) -> list[WorkflowStep]:
        """
        Create decision tree workflow.

        Args:
            decision_point: Description of the decision to be made
            branches: Dictionary of branch configurations
            decision_agent: Agent to make the decision
            analysis_timeout: Timeout for decision analysis
            branch_timeout: Timeout for branch execution

        Returns:
            List of workflow steps for the decision tree
        """
        decision_steps = []

        # Decision point step
        decision_step = self.create_step(
            name=f"Decision Point: {decision_point}",
            description=f"AI-driven decision making at: {decision_point}",
            agent_target=decision_agent,
            prompt_template=f"Analyze the current situation and make a decision about: {decision_point}",
            expected_response_type=ResponseType.DECISION_ANALYSIS,
            timeout_seconds=analysis_timeout,
            metadata={
                "decision_point": decision_point,
                "step_type": "decision",
            },
        )
        decision_steps.append(decision_step)

        # Branch steps
        for branch_name, branch_config in branches.items():
            branch_step = self.create_step(
                name=f"Branch: {branch_name}",
                description=f"Execute branch: {branch_name}",
                agent_target=branch_config.get("agent", decision_agent),
                prompt_template=branch_config.get("prompt", f"Execute the {branch_name} branch"),
                expected_response_type=ResponseType.BRANCH_EXECUTION,
                timeout_seconds=branch_timeout,
                dependencies=[decision_step.id],
                metadata={
                    "branch_name": branch_name,
                    "branch_config": branch_config,
                    "step_type": "branch",
                },
            )
            decision_steps.append(branch_step)

        return decision_steps


class AutonomousLoopBuilder(WorkflowStepBuilder):
    """
    Builder for autonomous workflow loops.

    Creates workflows that adapt and iterate based on AI responses
    with goal-oriented progression.
    """

    def create_autonomous_loop(
        self,
        goal: str,
        max_iterations: int = 10,
        assessment_agent: str = "Agent-1",
        action_agent: str = "Agent-2",
        assessment_timeout: int = 120,
        action_timeout: int = 300,
    ) -> list[WorkflowStep]:
        """
        Create autonomous workflow loop.

        Args:
            goal: Goal to work towards
            max_iterations: Maximum number of iterations
            assessment_agent: Agent responsible for goal assessment
            action_agent: Agent responsible for taking actions
            assessment_timeout: Timeout for assessment steps
            action_timeout: Timeout for action steps

        Returns:
            List of workflow steps for the autonomous loop
        """
        autonomous_steps = []

        for i in range(max_iterations):
            # Goal assessment step
            assessment_step = self.create_step(
                name=f"Autonomous Assessment - Iteration {i+1}",
                description=f"Assess progress toward goal: {goal}",
                agent_target=assessment_agent,
                prompt_template=f"Assess current progress toward goal: {goal}. What's the next best action?",
                expected_response_type=ResponseType.GOAL_ASSESSMENT,
                timeout_seconds=assessment_timeout,
                dependencies=[f"autonomous_action_{i-1}"] if i > 0 else [],
                metadata={
                    "iteration": i + 1,
                    "goal": goal,
                    "step_type": "assessment",
                    "max_iterations": max_iterations,
                },
            )
            autonomous_steps.append(assessment_step)

            # Action execution step
            action_step = self.create_step(
                name=f"Autonomous Action - Iteration {i+1}",
                description=f"Execute next action toward goal: {goal}",
                agent_target=action_agent,
                prompt_template=f"Execute the next action toward goal: {goal}",
                expected_response_type=ResponseType.ACTION_EXECUTION,
                timeout_seconds=action_timeout,
                dependencies=[assessment_step.id],
                metadata={
                    "iteration": i + 1,
                    "goal": goal,
                    "step_type": "action",
                    "max_iterations": max_iterations,
                },
            )
            autonomous_steps.append(action_step)

        return autonomous_steps
